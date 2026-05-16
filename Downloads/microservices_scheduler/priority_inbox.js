require("dotenv").config({ path: "./vehicle_scheduling/vehicle_scheduling/.env" });
const axios = require("axios");

const WEIGHTS = { Placement: 3, Result: 2, Event: 1 };

async function getToken() {
  const response = await axios.post(
    "http://4.224.186.213/evaluation-service/auth",
    {
      email: process.env.EMAIL,
      name: process.env.NAME,
      rollNo: process.env.ROLL_NO,
      clientID: process.env.CLIENT_ID,
      clientSecret: process.env.CLIENT_SECRET,
      accessCode: process.env.ACCESS_CODE,
    }
  );
  return response.data.access_token;
}

async function getTopNotifications(n = 10) {
  const token = await getToken();

  const { data } = await axios.get(
    "http://4.224.186.213/evaluation-service/notifications",
    {
      headers: { Authorization: `Bearer ${token}` },
    }
  );

  const top = data.notifications
    .sort((a, b) => {
      if (WEIGHTS[b.Type] !== WEIGHTS[a.Type])
        return WEIGHTS[b.Type] - WEIGHTS[a.Type];
      return new Date(b.Timestamp) - new Date(a.Timestamp);
    })
    .slice(0, n);

  console.log(`\nTop ${n} Priority Notifications:\n`);
  top.forEach((n, i) => {
    console.log(`${i + 1}. [${n.Type}] ${n.Message} - ${n.Timestamp}`);
  });
}

getTopNotifications(10);