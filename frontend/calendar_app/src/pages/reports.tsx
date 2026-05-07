import React from 'react';
import { useQuery } from '@tanstack/react-query';
const ReportsPage = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['reports'],
    queryFn: async () => {
      // TODO: Fetch data from API
      return null;
    },
  });
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading reports</div>;
  return (
    <div className="reports-page">
      <h1>Reports</h1>
      {/* TODO: Add page content */}
    </div>
  );
};

export default ReportsPage;