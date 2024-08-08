-- init.sql
CREATE TABLE IF NOT EXISTS detections (
    "Class" TEXT,
    "Timestamp" TEXT,
    "Frame" BIGINT,
    "BoundingBox_Coord_0" FLOAT,
    "BoundingBox_Coord_1" FLOAT,
    "BoundingBox_Coord_2" FLOAT,
    "BoundingBox_Coord_3" FLOAT,
    "Confidence" FLOAT
);