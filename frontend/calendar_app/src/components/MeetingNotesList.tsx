import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../services/api.service';

interface MeetingNotesListProps {
  onEdit?: (item: any) => void;
  onDelete?: (id: number) => void;
}

const MeetingNotesList: React.FC<MeetingNotesListProps> = ({ onEdit, onDelete }) => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['meetingnotes', page, search],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      params.append('page', page.toString());
      return apiService.get(`/api/v1/meetingnotess?${params.toString()}`);
    },
  });

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure?')) {
      try {
        await apiService.delete(`/api/v1/meetingnotess/${id}`);
        refetch();
        onDelete?.(id);
      } catch (err) {
        alert('Error deleting item');
      }
    }
  };

  if (isLoading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error.message}</div>;

  const items = data || [];

  return (
    <div className="meetingnoteslist">
      <h2>MeetingNotesList</h2>
      
      <div className="search-box">
        <input
          type="text"
          placeholder="Search..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
          className="form-control"
        />
      </div>

      <div className="table-responsive">
        <table className="table">
          <thead>
            <tr>
              <th>Summary</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item: any) => (
              <tr key={item.id}>
                <td>{item.summary}</td>
                <td>{item.createdAt}</td>
                <td className="actions">
                  <button 
                    className="btn btn-sm btn-info"
                    onClick={() => onEdit?.(item)}
                  >
                    Edit
                  </button>
                  <button 
                    className="btn btn-sm btn-danger"
                    onClick={() => handleDelete(item.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {items.length === 0 && <p className="no-data">No data found</p>}
    </div>
  );
};

export default MeetingNotesList;