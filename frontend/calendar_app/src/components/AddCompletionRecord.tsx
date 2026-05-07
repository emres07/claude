import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { apiService } from '../services/api.service';

interface AddCompletionRecordProps {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

const AddCompletionRecord: React.FC<AddCompletionRecordProps> = ({ onSuccess, onError }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const mutation = useMutation({
    mutationFn: async (data) => {
      return apiService.post('/api/v1/completionrecords', data);
    },
    onSuccess: () => {
      setFormData({ name: '',description: '' });
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
    <form onSubmit={handleSubmit} className="addcompletionrecord-form">
      <h2>Add New CompletionRecord</h2>
      
      <div className="form-group">
        <label htmlFor="name">
          Name
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
        <label htmlFor="description">
          Description
          
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder=""
          
          className="form-control"
        />
        {errors.description && <span className="error">{errors.description}</span>}
      </div>
      {errors.submit && <div className="error-message">{errors.submit}</div>}
      
      <button 
        type="submit" 
        disabled={mutation.isPending}
        className="btn btn-primary"
      >
        {mutation.isPending ? 'Saving...' : 'Create CompletionRecord'}
      </button>
    </form>
  );
};

export default AddCompletionRecord;