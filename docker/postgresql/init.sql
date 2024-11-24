DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'issue-db'
   ) THEN
      PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE "issue-db"');
   END IF;
END
$do$;



CREATE TABLE IF NOT EXISTS issue_state(
   id UUID PRIMARY KEY,
   name VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS issue(
   id UUID PRIMARY KEY,
   auth_user_id UUID,
   auth_user_agent_id UUID,
   status UUID,
   subject VARCHAR(255),
   description TEXT,
   created_at TIMESTAMP WITH TIME ZONE,
   closed_at TIMESTAMP WITH TIME ZONE,
   channel_plan_id UUID,
   CONSTRAINT fk_status
        FOREIGN KEY (status) 
        REFERENCES issue_state (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS issue_attachment (
    id UUID PRIMARY KEY,
    file_path VARCHAR(255),
    issue_id UUID,
    CONSTRAINT fk_issue
        FOREIGN KEY (issue_id) 
        REFERENCES issue (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS issue_trace (
    id UUID PRIMARY KEY, 
    issue_id UUID,
    auth_user_id UUID  NULL,
    auth_user_agent_id UUID  NULL,
    scope VARCHAR(255),
    channel_plan_id UUID,
    created_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_issue
        FOREIGN KEY (issue_id) 
        REFERENCES issue (id)
        ON DELETE CASCADE
);
