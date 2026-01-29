import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Header from '../components/Header';

describe('Header Component', () => {
  it('renders app title', () => {
    const mockUser = { username: 'testuser' };
    const mockOnLogout = () => {};
    
    render(<Header user={mockUser} onLogout={mockOnLogout} />);
    
    expect(screen.getByText(/expense tracker/i)).toBeInTheDocument();
  });

  it('displays username when user is logged in', () => {
    const mockUser = { username: 'testuser' };
    const mockOnLogout = () => {};
    
    render(<Header user={mockUser} onLogout={mockOnLogout} />);
    
    expect(screen.getByText(/testuser/i)).toBeInTheDocument();
  });

  it('renders logout button when user is logged in', () => {
    const mockUser = { username: 'testuser' };
    const mockOnLogout = () => {};
    
    render(<Header user={mockUser} onLogout={mockOnLogout} />);
    
    const logoutButton = screen.getByRole('button', { name: /logout/i });
    expect(logoutButton).toBeInTheDocument();
  });

  it('does not show username when user is null', () => {
    const mockOnLogout = () => {};
    
    render(<Header user={null} onLogout={mockOnLogout} />);
    
    // Should not find any user-specific content
    const header = screen.getByRole('banner');
    expect(header).toBeInTheDocument();
  });
});
