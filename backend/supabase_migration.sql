-- =========================================
-- Supabase Database Migration Script
-- Expense Tracker Application
-- =========================================
-- Run this in Supabase Dashboard → SQL Editor
-- Enable UUID extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================================
-- Table: users
-- =========================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- Table: expenses
-- =========================================
CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    category VARCHAR NOT NULL,
    amount FLOAT NOT NULL,
    date DATE NOT NULL,
    description VARCHAR,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- Table: budgets
-- =========================================
CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    category VARCHAR NOT NULL,
    limit_amount FLOAT NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- Table: debts
-- =========================================
CREATE TABLE IF NOT EXISTS debts (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    principal_amount FLOAT NOT NULL,
    interest_rate FLOAT NOT NULL,
    emi_amount FLOAT NOT NULL,
    emi_date INTEGER NOT NULL,
    start_date DATE NOT NULL,
    remaining_amount FLOAT NOT NULL,
    status VARCHAR DEFAULT 'active',
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- Table: friendships
-- =========================================
CREATE TABLE IF NOT EXISTS friendships (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    friend_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- Table: split_expenses
-- =========================================
CREATE TABLE IF NOT EXISTS split_expenses (
    id SERIAL PRIMARY KEY,
    description VARCHAR NOT NULL,
    total_amount FLOAT NOT NULL,
    category VARCHAR NOT NULL,
    date DATE NOT NULL,
    created_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- Table: split_participants (junction table)
-- =========================================
CREATE TABLE IF NOT EXISTS split_participants (
    split_expense_id INTEGER NOT NULL REFERENCES split_expenses(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (split_expense_id, user_id)
);

-- =========================================
-- Table: settlements
-- =========================================
CREATE TABLE IF NOT EXISTS settlements (
    id SERIAL PRIMARY KEY,
    from_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    to_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- Table: transactions (for payment gateway)
-- =========================================
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stripe_payment_intent_id VARCHAR UNIQUE,
    amount FLOAT NOT NULL,
    currency VARCHAR DEFAULT 'INR',
    payment_method VARCHAR NOT NULL,
    transaction_type VARCHAR NOT NULL,
    debt_id INTEGER REFERENCES debts(id) ON DELETE SET NULL,
    split_expense_id INTEGER REFERENCES split_expenses(id) ON DELETE SET NULL,
    status VARCHAR DEFAULT 'pending',
    description VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- Table: groups
-- =========================================
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    currency VARCHAR DEFAULT 'INR' NOT NULL,
    image_url VARCHAR,
    is_active BOOLEAN DEFAULT true,
    created_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- Table: group_members
-- =========================================
CREATE TABLE IF NOT EXISTS group_members (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR DEFAULT 'member' NOT NULL,
    status VARCHAR DEFAULT 'pending' NOT NULL,
    joined_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(group_id, user_id)
);

-- =========================================
-- Table: group_expenses
-- =========================================
CREATE TABLE IF NOT EXISTS group_expenses (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    description VARCHAR NOT NULL,
    total_amount FLOAT NOT NULL,
    category VARCHAR NOT NULL,
    date DATE NOT NULL,
    paid_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- Table: group_expense_participants
-- =========================================
CREATE TABLE IF NOT EXISTS group_expense_participants (
    id SERIAL PRIMARY KEY,
    group_expense_id INTEGER NOT NULL REFERENCES group_expenses(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    share_amount FLOAT NOT NULL,
    UNIQUE(group_expense_id, user_id)
);

-- =========================================
-- Table: group_settlements
-- =========================================
CREATE TABLE IF NOT EXISTS group_settlements (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    from_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    to_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =========================================
-- Indexes for better query performance
-- =========================================
CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id);
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date);
CREATE INDEX IF NOT EXISTS idx_budgets_user_id ON budgets(user_id);
CREATE INDEX IF NOT EXISTS idx_debts_user_id ON debts(user_id);
CREATE INDEX IF NOT EXISTS idx_friendships_user_id ON friendships(user_id);
CREATE INDEX IF NOT EXISTS idx_friendships_friend_id ON friendships(friend_id);
CREATE INDEX IF NOT EXISTS idx_split_expenses_created_by ON split_expenses(created_by);
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_groups_created_by ON groups(created_by);
CREATE INDEX IF NOT EXISTS idx_group_members_group_id ON group_members(group_id);
CREATE INDEX IF NOT EXISTS idx_group_members_user_id ON group_members(user_id);
CREATE INDEX IF NOT EXISTS idx_group_members_status ON group_members(status);
CREATE INDEX IF NOT EXISTS idx_group_expenses_group_id ON group_expenses(group_id);
CREATE INDEX IF NOT EXISTS idx_group_expenses_paid_by ON group_expenses(paid_by);
CREATE INDEX IF NOT EXISTS idx_group_expense_participants_expense_id ON group_expense_participants(group_expense_id);
CREATE INDEX IF NOT EXISTS idx_group_settlements_group_id ON group_settlements(group_id);

-- =========================================
-- Enable Row Level Security (RLS)
-- =========================================
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE expenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE budgets ENABLE ROW LEVEL SECURITY;
ALTER TABLE debts ENABLE ROW LEVEL SECURITY;
ALTER TABLE friendships ENABLE ROW LEVEL SECURITY;
ALTER TABLE split_expenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE split_participants ENABLE ROW LEVEL SECURITY;
ALTER TABLE settlements ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE groups ENABLE ROW LEVEL SECURITY;
ALTER TABLE group_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE group_expenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE group_expense_participants ENABLE ROW LEVEL SECURITY;
ALTER TABLE group_settlements ENABLE ROW LEVEL SECURITY;

-- =========================================
-- RLS Policies (Basic - Users can access their own data)
-- =========================================

-- Users table policies
CREATE POLICY "Users can view their own profile" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update their own profile" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- Expenses table policies
CREATE POLICY "Users can view their own expenses" ON expenses
    FOR ALL USING (user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text));

-- Budgets table policies
CREATE POLICY "Users can manage their own budgets" ON budgets
    FOR ALL USING (user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text));

-- Debts table policies
CREATE POLICY "Users can manage their own debts" ON debts
    FOR ALL USING (user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text));

-- Friendships table policies
CREATE POLICY "Users can view their friendships" ON friendships
    FOR SELECT USING (user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text)
                   OR friend_id = (SELECT id FROM users WHERE auth.uid()::text = id::text));

CREATE POLICY "Users can create friendships" ON friendships
    FOR INSERT WITH CHECK (user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text));

-- Split expenses policies
CREATE POLICY "Users can view split expenses they're part of" ON split_expenses
    FOR SELECT USING (
        created_by = (SELECT id FROM users WHERE auth.uid()::text = id::text)
        OR id IN (SELECT split_expense_id FROM split_participants
                  WHERE user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text))
    );

-- Transactions policies
CREATE POLICY "Users can view their own transactions" ON transactions
    FOR ALL USING (user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text));

-- =========================================
-- Group-related RLS Policies
-- =========================================

-- Groups policies
CREATE POLICY "Users can view groups they are members of" ON groups
    FOR SELECT USING (
        id IN (SELECT group_id FROM group_members
               WHERE user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text)
               AND status = 'accepted')
    );

CREATE POLICY "Users can create groups" ON groups
    FOR INSERT WITH CHECK (created_by = (SELECT id FROM users WHERE auth.uid()::text = id::text));

CREATE POLICY "Group admins can update groups" ON groups
    FOR UPDATE USING (
        id IN (SELECT group_id FROM group_members
               WHERE user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text)
               AND role = 'admin' AND status = 'accepted')
    );

-- Group members policies
CREATE POLICY "Users can view members of their groups" ON group_members
    FOR SELECT USING (
        group_id IN (SELECT group_id FROM group_members gm
                     WHERE gm.user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text)
                     AND gm.status = 'accepted')
        OR user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text)
    );

CREATE POLICY "Group members can invite others" ON group_members
    FOR INSERT WITH CHECK (
        group_id IN (SELECT group_id FROM group_members
                     WHERE user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text)
                     AND status = 'accepted')
    );

CREATE POLICY "Users can update their own membership" ON group_members
    FOR UPDATE USING (user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text));

-- Group expenses policies
CREATE POLICY "Group members can view group expenses" ON group_expenses
    FOR SELECT USING (
        group_id IN (SELECT group_id FROM group_members
                     WHERE user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text)
                     AND status = 'accepted')
    );

CREATE POLICY "Group members can create expenses" ON group_expenses
    FOR INSERT WITH CHECK (
        group_id IN (SELECT group_id FROM group_members
                     WHERE user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text)
                     AND status = 'accepted')
    );

-- Group expense participants policies
CREATE POLICY "Group members can view expense participants" ON group_expense_participants
    FOR SELECT USING (
        group_expense_id IN (
            SELECT ge.id FROM group_expenses ge
            JOIN group_members gm ON ge.group_id = gm.group_id
            WHERE gm.user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text)
            AND gm.status = 'accepted'
        )
    );

-- Group settlements policies
CREATE POLICY "Group members can view settlements" ON group_settlements
    FOR SELECT USING (
        group_id IN (SELECT group_id FROM group_members
                     WHERE user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text)
                     AND status = 'accepted')
    );

CREATE POLICY "Group members can create settlements" ON group_settlements
    FOR INSERT WITH CHECK (
        group_id IN (SELECT group_id FROM group_members
                     WHERE user_id = (SELECT id FROM users WHERE auth.uid()::text = id::text)
                     AND status = 'accepted')
    );

-- =========================================
-- Success message
-- =========================================
DO $$
BEGIN
    RAISE NOTICE '✅ Database migration completed successfully!';
    RAISE NOTICE '📋 All tables, indexes, and RLS policies have been created.';
    RAISE NOTICE '👥 Group system tables added: groups, group_members, group_expenses, group_expense_participants, group_settlements';
END $$;
