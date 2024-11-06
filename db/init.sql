CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING'
);

-- Insert initial data into tasks table
INSERT INTO tasks (title, description, status) VALUES
    ('First Task', 'This is the first task', 'PENDING'),
    ('Second Task', 'This is the second task', 'DONE');
