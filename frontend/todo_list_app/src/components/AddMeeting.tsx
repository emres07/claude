import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { apiService } from '../services/api.service';

interface AddMeetingProps {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

const AddMeeting: React.FC<AddMeetingProps> = ({ onSuccess, onError }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    startTime: '',
    endTime: '',
    location: '',
    });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const mutation = useMutation({
    mutationFn: async (data) => {
      return apiService.post('/api/v1/meetings', data);
    },
    onSuccess: () => {
      setFormData({ title: '',description: '',startTime: '',endTime: '',location: '' });
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
    <form onSubmit={handleSubmit} className="addmeeting-form">
      <h2>Add New Meeting</h2>
      
      <div className="form-group">
        <label htmlFor="title">
          Meeting Title
          <span className="required">*</span>
        </label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder=""
          required
          className="form-control"
        />
        {errors.title && <span className="error">{errors.title}</span>}
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
      <div className="form-group">
        <label htmlFor="startTime">
          Start Time
          <span className="required">*</span>
        </label>
        <input
          type="datetime-local"
          id="startTime"
          name="startTime"
          value={formData.startTime}
          onChange={handleChange}
          placeholder=""
          required
          className="form-control"
        />
        {errors.startTime && <span className="error">{errors.startTime}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="endTime">
          End Time
          <span className="required">*</span>
        </label>
        <input
          type="datetime-local"
          id="endTime"
          name="endTime"
          value={formData.endTime}
          onChange={handleChange}
          placeholder=""
          required
          className="form-control"
        />
        {errors.endTime && <span className="error">{errors.endTime}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="location">
          Location
          
        </label>
        <input
          type="text"
          id="location"
          name="location"
          value={formData.location}
          onChange={handleChange}
          placeholder=""
          
          className="form-control"
        />
        {errors.location && <span className="error">{errors.location}</span>}
      </div>
      {errors.submit && <div className="error-message">{errors.submit}</div>}
      
      <button 
        type="submit" 
        disabled={mutation.isPending}
        className="btn btn-primary"
      >
        {mutation.isPending ? 'Saving...' : 'Create Meeting'}
      </button>
    </form>
  );
};

export default AddMeeting;