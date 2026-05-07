import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { apiService } from '../services/api.service';

interface AddMeetingNotesProps {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

const AddMeetingNotes: React.FC<AddMeetingNotesProps> = ({ onSuccess, onError }) => {
  const [formData, setFormData] = useState({
    content: '',
    summary: '',
    });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const mutation = useMutation({
    mutationFn: async (data) => {
      return apiService.post('/api/v1/meetingnotess', data);
    },
    onSuccess: () => {
      setFormData({ content: '',summary: '' });
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
    <form onSubmit={handleSubmit} className="addmeetingnotes-form">
      <h2>Add New MeetingNotes</h2>
      
      <div className="form-group">
        <label htmlFor="content">
          Notes Content
          <span className="required">*</span>
        </label>
        <textarea
          id="content"
          name="content"
          value={formData.content}
          onChange={handleChange}
          placeholder=""
          required
          className="form-control"
        />
        {errors.content && <span className="error">{errors.content}</span>}
      </div>
      <div className="form-group">
        <label htmlFor="summary">
          Summary
          
        </label>
        <textarea
          id="summary"
          name="summary"
          value={formData.summary}
          onChange={handleChange}
          placeholder=""
          
          className="form-control"
        />
        {errors.summary && <span className="error">{errors.summary}</span>}
      </div>
      {errors.submit && <div className="error-message">{errors.submit}</div>}
      
      <button 
        type="submit" 
        disabled={mutation.isPending}
        className="btn btn-primary"
      >
        {mutation.isPending ? 'Saving...' : 'Create MeetingNotes'}
      </button>
    </form>
  );
};

export default AddMeetingNotes;