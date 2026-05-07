import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { apiService } from '../services/api.service';

interface AddUserProps {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

const AddUser: React.FC<AddUserProps> = ({ onSuccess, onError }) => {
  const [formData, setFormData] = useState({
    email: '',
    name: '',
    password: '',
    });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const mutation = useMutation({
    mutationFn: async (data) => {
      return apiService.post('/api/v1/users', data);
    },
    onSuccess: () => {
      setFormData({ email: '',name: '',password: '' });
      onSuccess?.();
    },
    onError: (error: Error) => {
      setErrors({ submit: error.message });
      onError?.(error);
    },
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="adduser-form">
      <h2>Add New User</h2>
      
      <div className="form-group">
        <label htmlFor="email">
          Email
          <span className="required">*</span>
        </label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder=""
          required
          className="form-control"
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="name">
          Full Name
          <span className="required">*</span>
        </label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder=""
          required
          className="form-control"
        />
        {errors.name && <span className="error">{errors.name}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="password">
          Password
          <span className="required">*</span>
        </label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder=""
          required
          className="form-control"
        />
        {errors.password && <span className="error">{errors.password}</span>}
      </div>
      {errors.submit && <div className="error-message">{errors.submit}</div>}
      
      <button 
        type="submit" 
        disabled={mutation.isPending}
        className="btn btn-primary"
      >
        {mutation.isPending ? 'Saving...' : 'Create User'}
      </button>
    </form>
  );
};

export default AddUser;