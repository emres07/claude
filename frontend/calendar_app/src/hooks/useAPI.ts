import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '../services/api.service';

interface UseAPIOptions {
  enabled?: boolean;
  refetchInterval?: number;
}

export function useAPI<T>(
  endpoint: string,
  options?: UseAPIOptions
) {
  return useQuery<T>({
    queryKey: [endpoint],
    queryFn: () => apiService.get<T>(endpoint),
    enabled: options?.enabled !== false,
    refetchInterval: options?.refetchInterval,
  });
}

export function useCreate<T>(endpoint: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: any) => apiService.post<T>(endpoint, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [endpoint] });
    },
  });
}

export function useUpdate<T>(endpoint: string, id: number) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: any) => apiService.put<T>(`${endpoint}/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [endpoint] });
    },
  });
}

export function useDelete(endpoint: string, id: number) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => apiService.delete(`${endpoint}/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [endpoint] });
    },
  });
}