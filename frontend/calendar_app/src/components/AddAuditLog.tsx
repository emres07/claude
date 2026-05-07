import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { apiService } from '../services/api.service';

interface AddAuditLogProps {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

const AddAuditLog: React.FC<AddAuditLogProps> = ({ onSuccess, onError }) => {
  const [formData, setFormData] = useState({
    entityType: '',
    operation: '',
    changes: '',
    });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const mutation = useMutation({
    mutationFn: async (data) => {
      return apiService.post('/api/v1/auditlogs', data);
    },
    onSuccess: () => {
      setFormData({ entityType: '',operation: '',changes: '' });
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
    <form onSubmit={handleSubmit} className="addauditlog-form">
      <h2>Add New AuditLog</h2>
      
      <div className="form-group">
        <label htmlFor="entityType">
          Entity Type
          <span className="required">*</span>
        </label>
        <input
          type="text"
          id="entityType"
          name="entityType"
          value={formData.entityType}
          onChange={handleChange}
          placeholder=""
          required
          className="form-control"
        />
        {errors.entityType && <span className="error">{errors.entityType}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="operation">
          Operation
          <span className="required">*</span>
        </label>
        <input
          type="text"
          id="operation"
          name="operation"
          value={formData.operation}
          onChange={handleChange}
          placeholder=""
          required
          className="form-control"
        />
        {errors.operation && <span className="error">{errors.operation}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="changes">
          Changes
          
        </label>
        <textarea
          id="changes"
          name="changes"
          value={formData.changes}
          onChange={handleChange}
          placeholder=""
          
          className="form-control"
        />
        {errors.changes && <span className="error">{errors.changes}</span>}
      </div>
      {errors.submit && <div className="error-message">{errors.submit}</div>}
      
      <button 
        type="submit" 
        disabled={mutation.isPending}
        className="btn btn-primary"
      >
        {mutation.isPending ? 'Saving...' : 'Create AuditLog'}
      </button>
    </form>
  );
};

export default AddAuditLog;