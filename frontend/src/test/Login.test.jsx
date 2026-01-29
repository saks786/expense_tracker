import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from '../components/Login';

// Mock the API
vi.mock('../api', () => ({
  login: vi.fn(),
}));

const renderLogin = () => {
  return render(
    <BrowserRouter>
      <Login />
    </BrowserRouter>
  );
};

describe('Login Component', () => {
  it('renders login form correctly', () => {
    renderLogin();
    
    expect(screen.getByPlaceholderText(/username/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  it('updates form fields on input', () => {
    renderLogin();
    
    const usernameInput = screen.getByPlaceholderText(/username/i);
    const passwordInput = screen.getByPlaceholderText(/password/i);
    
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    
    expect(usernameInput.value).toBe('testuser');
    expect(passwordInput.value).toBe('password123');
  });

  it('displays login button', () => {
    renderLogin();
    
    const loginButton = screen.getByRole('button', { name: /login/i });
    expect(loginButton).toBeInTheDocument();
    expect(loginButton).not.toBeDisabled();
  });

  it('has link to register page', () => {
    renderLogin();
    
    const registerLink = screen.getByText(/register/i);
    expect(registerLink).toBeInTheDocument();
  });
});
