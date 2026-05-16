# Stage 1

## REST API Design for Campus Notification Platform

### Endpoints

#### Get All Notifications
- **GET** `/api/notifications`
- **Headers:** `Authorization: Bearer <token>`
- **Response:**
```json
{
  "notifications": [
    {
      "id": "uuid",
      "type": "Placement|Event|Result",
      "message": "string",
      "timestamp": "2026-01-01T00:00:00Z",
      "isRead": false
    }
  ]
}
```

#### Mark Notification as Read
- **PATCH** `/api/notifications/:id/read`
- **Headers:** `Authorization: Bearer <token>`

#### Real-time: WebSocket
- Connect to `ws://server/notifications`
- Server pushes new notifications instantly

---

# Stage 2

## Database Design

**Recommended DB:** PostgreSQL

### Schema
```sql
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  studentID INT NOT NULL,
  type notification_type NOT NULL,
  message TEXT NOT NULL,
  isRead BOOLEAN DEFAULT false,
  createdAt TIMESTAMP DEFAULT NOW()
);

CREATE TYPE notification_type AS ENUM ('Event', 'Result', 'Placement');
```

### Scaling Problems & Solutions
- Add indexes on `studentID` and `createdAt`
- Use pagination to limit results
- Archive old notifications

---

# Stage 3

## Query Analysis

**Original Query:**
```sql
SELECT * FROM notifications
WHERE studentID = 1042 AND isRead = false
ORDER BY createdAt DESC;
```

**Problems:**
- `SELECT *` fetches unnecessary columns
- No index on `studentID` or `isRead`

**Fix:**
```sql
CREATE INDEX idx_student_unread 
ON notifications(studentID, isRead, createdAt DESC);

SELECT id, type, message, createdAt 
FROM notifications
WHERE studentID = 1042 AND isRead = false
ORDER BY createdAt DESC;
```

**Adding indexes on every column is NOT advised** — it slows down writes.

**Placement notifications last 7 days:**
```sql
SELECT * FROM notifications
WHERE type = 'Placement'
AND createdAt >= NOW() - INTERVAL '7 days';
```

---

# Stage 4

## Caching Strategy

**Problem:** DB overwhelmed on every page load.

**Solution:** Use Redis caching
- Cache notifications per student for 60 seconds
- Invalidate cache when new notification arrives
- Use pagination (limit 20 per page)

**Tradeoffs:**
- Redis adds complexity but reduces DB load significantly
- Slight delay in seeing newest notifications (acceptable)

---

# Stage 5

## Bulk Notification Redesign

**Problems with current implementation:**
- Sequential processing is slow for 50,000 students
- If `send_email` fails midway, no retry mechanism
- All three operations coupled together

**Revised Pseudocode:**
