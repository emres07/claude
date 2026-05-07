import React from 'react';
import { useQuery } from '@tanstack/react-query';
const SchedulingPage = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['scheduling'],
    queryFn: async () => {
      // TODO: Fetch data from API
      return null;
    },
  });
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading scheduling</div>;
  return (
    <div className="scheduling-page">
      <h1>Scheduling</h1>
      {/* TODO: Add page content */}
    </div>
  );
};

export default SchedulingPage;