import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import DebtList from '../components/DebtList';

// Mock the API
vi.mock('../api', () => ({
  getDebts: vi.fn(),
  deleteDebt: vi.fn(),
  updateDebt: vi.fn(),
}));

describe('DebtList Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('displays empty state when no debts', async () => {
    const { getDebts } = await import('../api');
    getDebts.mockResolvedValue([]);
    
    const mockOnPaymentClick = vi.fn();
    render(<DebtList refresh={0} onPaymentClick={mockOnPaymentClick} />);
    
    await waitFor(() => {
      expect(screen.getByText(/no debts tracked yet/i)).toBeInTheDocument();
    });
  });

  it('renders debt list container', async () => {
    const { getDebts } = await import('../api');
    getDebts.mockResolvedValue([]);
    
    const mockOnPaymentClick = vi.fn();
    const { container } = render(<DebtList refresh={0} onPaymentClick={mockOnPaymentClick} />);
    
    // Check that the debt list container exists
    expect(container.querySelector('.debt-list')).toBeInTheDocument();
  });
});
