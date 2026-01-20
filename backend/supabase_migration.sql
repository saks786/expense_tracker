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
-- Success message
-- =========================================
DO $$
BEGIN
    RAISE NOTICE '✅ Database migration completed successfully!';
    RAISE NOTICE '📋 All tables, indexes, and RLS policies have been created.';
END $$;
