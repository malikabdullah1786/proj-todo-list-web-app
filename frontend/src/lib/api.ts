import { useState } from 'react';

export const apiFetch = async (endpoint: string, options: RequestInit = {}) => {
  const response = await fetch(`http://localhost:8000${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Something went wrong');
  }
  return response.json();
};
