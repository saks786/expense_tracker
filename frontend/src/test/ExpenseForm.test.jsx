import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ExpenseForm from '../components/ExpenseForm';

describe('ExpenseForm Component', () => {
  it('renders all form fields', () => {
    const mockOnAdd = vi.fn();
    render(<ExpenseForm onAdd={mockOnAdd} />);
    
    expect(screen.getByLabelText(/category/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/amount/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
  });

  it('displays all expense categories', () => {
    const mockOnAdd = vi.fn();
    render(<ExpenseForm onAdd={mockOnAdd} />);
    
    const categorySelect = screen.getByLabelText(/category/i);
    const options = categorySelect.querySelectorAll('option');
    
    // Should have 8 options (placeholder + 7 categories)
    expect(options.length).toBeGreaterThan(7);
    expect(screen.getByText('Food')).toBeInTheDocument();
    expect(screen.getByText('Transport')).toBeInTheDocument();
    expect(screen.getByText('Entertainment')).toBeInTheDocument();
  });

  it('updates amount field on input', () => {
    const mockOnAdd = vi.fn();
    render(<ExpenseForm onAdd={mockOnAdd} />);
    
    const amountInput = screen.getByLabelText(/amount/i);
    fireEvent.change(amountInput, { target: { value: '100' } });
    
    expect(amountInput.value).toBe('100');
  });

  it('updates description field on input', () => {
    const mockOnAdd = vi.fn();
    render(<ExpenseForm onAdd={mockOnAdd} />);
    
    const descInput = screen.getByLabelText(/description/i);
    fireEvent.change(descInput, { target: { value: 'Test expense' } });
    
    expect(descInput.value).toBe('Test expense');
  });

  it('has submit button', () => {
    const mockOnAdd = vi.fn();
    render(<ExpenseForm onAdd={mockOnAdd} />);
    
    const submitButton = screen.getByRole('button', { name: /add expense/i });
    expect(submitButton).toBeInTheDocument();
  });
});
