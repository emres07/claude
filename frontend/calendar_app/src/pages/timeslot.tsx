import React, { useState } from 'react';
import AddTimeSlot from '../components/AddTimeSlot';
import TimeSlotList from '../components/TimeSlotList';
const TimeslotPage = () => {
  const [mode, setMode] = useState<'view' | 'edit' | 'add'>('view');
  const [selectedItem, setSelectedItem] = useState<any>(null);

  const handleAdd = () => {
    setSelectedItem(null);
    setMode('add');
  };

  const handleEdit = (item: any) => {
    setSelectedItem(item);
    setMode('edit');
  };

  const handleSuccess = () => {
    setMode('view');
    setSelectedItem(null);
  };

  return (
    <div className="timeslot-page">
      <div className="page-header">
        <h1>timeslot</h1>
        {mode === 'view' && (
          <button className="btn btn-primary" onClick={handleAdd}>
            + Add New
          </button>
        )}
      </div>

      <div className="page-content">
        {mode === 'view' && (
          <TimeSlotList
            onEdit={handleEdit}
            onDelete={() => setMode('view')}
          />
        )}

        {(mode === 'add' || mode === 'edit') && (
          <div className="form-container">
            <button 
              className="btn btn-secondary btn-back"
              onClick={() => setMode('view')}
            >
              ← Back
            </button>
            <AddTimeSlot
              data={selectedItem}
              onSuccess={handleSuccess}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default TimeslotPage;