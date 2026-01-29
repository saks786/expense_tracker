import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import ExpenseList from '../components/ExpenseList';

describe('ExpenseList Component', () => {
  it('displays empty state when no expenses', () => {
    const mockOnUpdate = vi.fn();
    render(<ExpenseList expenses={[]} onUpdate={mockOnUpdate} />);
    
    expect(screen.getByText(/no expenses yet/i)).toBeInTheDocument();
  });

  it('renders expense items when expenses exist', () => {
    const mockExpenses = [
      {
        id: 1,
        category: 'Food',
        amount: 100,
        description: 'Lunch',
        date: '2026-01-29',
      },
      {
        id: 2,
        category: 'Transport',
        amount: 50,
        description: 'Taxi',
        date: '2026-01-28',
      },
    ];
    
    const mockOnUpdate = vi.fn();
    render(<ExpenseList expenses={mockExpenses} onUpdate={mockOnUpdate} />);
    
    expect(screen.getByText('Lunch')).toBeInTheDocument();
    expect(screen.getByText('Taxi')).toBeInTheDocument();
    expect(screen.getByText(/₹100/)).toBeInTheDocument();
    expect(screen.getByText(/₹50/)).toBeInTheDocument();
  });

  it('displays expense categories correctly', () => {
    const mockExpenses = [
      {
        id: 1,
        category: 'Food',
        amount: 100,
        description: 'Lunch',
        date: '2026-01-29',
      },
    ];
    
    const mockOnUpdate = vi.fn();
    render(<ExpenseList expenses={mockExpenses} onUpdate={mockOnUpdate} />);
    
    expect(screen.getByText('Food')).toBeInTheDocument();
  });

  it('renders edit and delete buttons for each expense', () => {
    const mockExpenses = [
      {
        id: 1,
        category: 'Food',
        amount: 100,
        description: 'Lunch',
        date: '2026-01-29',
      },
    ];
    
    const mockOnUpdate = vi.fn();
    render(<ExpenseList expenses={mockExpenses} onUpdate={mockOnUpdate} />);
    
    const editButtons = screen.getAllByRole('button', { name: /✏️/i });
    const deleteButtons = screen.getAllByRole('button', { name: /🗑️/i });
    
    expect(editButtons).toHaveLength(1);
    expect(deleteButtons).toHaveLength(1);
  });
});
