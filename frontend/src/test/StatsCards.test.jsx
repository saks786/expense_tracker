import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import StatsCards from '../components/StatsCards';

describe('StatsCards Component', () => {
  it('renders all stat cards', () => {
    const mockExpenses = [
      { amount: 500, date: '2026-01-29', category: 'Food' },
      { amount: 1000, date: '2026-01-28', category: 'Transport' },
    ];
    
    render(<StatsCards expenses={mockExpenses} />);
    
    expect(screen.getByText(/total spent/i)).toBeInTheDocument();
    expect(screen.getByText(/monthly spend/i)).toBeInTheDocument();
    expect(screen.getByText(/average/i)).toBeInTheDocument();
  });

  it('displays transaction counts correctly', () => {
    const mockExpenses = [
      { amount: 500, date: '2026-01-29', category: 'Food' },
      { amount: 1000, date: '2026-01-28', category: 'Transport' },
    ];
    
    render(<StatsCards expenses={mockExpenses} />);
    
    // Should show 2 transactions
    expect(screen.getByText(/2/)).toBeInTheDocument();
    expect(screen.getByText(/transactions/i)).toBeInTheDocument();
  });

  it('handles empty expenses array', () => {
    const mockExpenses = [];
    
    render(<StatsCards expenses={mockExpenses} />);
    
    // Should render transactions text
    expect(screen.getByText(/transactions/i)).toBeInTheDocument();
  });
});
