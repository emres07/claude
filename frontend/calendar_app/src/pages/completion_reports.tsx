import React from 'react';
import { useQuery } from '@tanstack/react-query';
const CompletionReportsPage = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['completion_reports'],
    queryFn: async () => {
      // TODO: Fetch data from API
      return null;
    },
  });
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading completion_reports</div>;
  return (
    <div className="completion_reports-page">
      <h1>CompletionReports</h1>
      {/* TODO: Add page content */}
    </div>
  );
};

export default CompletionReportsPage;