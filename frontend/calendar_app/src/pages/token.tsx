import React, { useState } from 'react';
import AddToken from '../components/AddToken';
import TokenList from '../components/TokenList';
const TokenPage = () => {
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
    <div className="token-page">
      <div className="page-header">
        <h1>token</h1>
        {mode === 'view' && (
          <button className="btn btn-primary" onClick={handleAdd}>
            + Add New
          </button>
        )}
      </div>

      <div className="page-content">
        {mode === 'view' && (
          <TokenList
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
            <AddToken
              data={selectedItem}
              onSuccess={handleSuccess}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default TokenPage;