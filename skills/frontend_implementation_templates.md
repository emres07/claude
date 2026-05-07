# Frontend Implementation Templates - Jinja2 Format

## Component Implementation - Add/Create Form

<!-- component_add_form -->
```typescript
import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
{% if imports %}
{% for imp in imports -%}
import {{ imp }};
{% endfor %}
{% endif -%}
import { apiService } from '../services/api.service';

interface {{ component_name }}Props {
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

const {{ component_name }}: React.FC<{{ component_name }}Props> = ({ onSuccess, onError }) => {
  const [formData, setFormData] = useState({
    {% for field in fields -%}
    {{ field.name }}: '',
    {% endfor -%}
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const mutation = useMutation({
    mutationFn: async (data) => {
      return apiService.post('{{ api_endpoint }}', data);
    },
    onSuccess: () => {
      setFormData({ {% for field in fields %}{{ field.name }}: ''{{ "," if not loop.last }}{% endfor %} });
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
    <form onSubmit={handleSubmit} className="{{ component_name_kebab }}-form">
      <h2>{{ form_title | default(component_name) }}</h2>
      
      {% for field in fields -%}
      <div className="form-group">
        <label htmlFor="{{ field.name }}">
          {{ field.label | default(field.name | capitalize) }}
          {% if field.required %}<span className="required">*</span>{% endif %}
        </label>
        {% if field.type == 'textarea' -%}
        <textarea
          id="{{ field.name }}"
          name="{{ field.name }}"
          value={formData.{{ field.name }}}
          onChange={handleChange}
          placeholder="{{ field.placeholder | default('') }}"
          {% if field.required %}required{% endif %}
          className="form-control"
        />
        {% else -%}
        <input
          type="{{ field.input_type | default('text') }}"
          id="{{ field.name }}"
          name="{{ field.name }}"
          value={formData.{{ field.name }}}
          onChange={handleChange}
          placeholder="{{ field.placeholder | default('') }}"
          {% if field.required %}required{% endif %}
          className="form-control"
        />
        {% endif -%}
        {errors.{{ field.name }} && <span className="error">{errors.{{ field.name }}}</span>}
      </div>
      {% endfor -%}

      {errors.submit && <div className="error-message">{errors.submit}</div>}
      
      <button 
        type="submit" 
        disabled={mutation.isPending}
        className="btn btn-primary"
      >
        {mutation.isPending ? 'Saving...' : '{{ submit_button_text | default("Save") }}'}
      </button>
    </form>
  );
};

export default {{ component_name }};
```
<!-- /component_add_form -->

## Component Implementation - List/Table

<!-- component_list -->
```typescript
import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
{% if imports %}
{% for imp in imports -%}
import {{ imp }};
{% endfor %}
{% endif -%}
import { apiService } from '../services/api.service';

interface {{ component_name }}Props {
  onEdit?: (item: any) => void;
  onDelete?: (id: number) => void;
}

const {{ component_name }}: React.FC<{{ component_name }}Props> = ({ onEdit, onDelete }) => {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['{{ endpoint_singular }}', page, search],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      params.append('page', page.toString());
      return apiService.get(`{{ api_endpoint }}?${params.toString()}`);
    },
  });

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure?')) {
      try {
        await apiService.delete(`{{ api_endpoint }}/${id}`);
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
    <div className="{{ component_name_kebab }}">
      <h2>{{ list_title | default(component_name) }}</h2>
      
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
              {% for field in display_fields -%}
              <th>{{ field.label | default(field.name | capitalize) }}</th>
              {% endfor -%}
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item: any) => (
              <tr key={item.id}>
                {% for field in display_fields -%}
                <td>{item.{{ field.name }}}</td>
                {% endfor -%}
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

export default {{ component_name }};
```
<!-- /component_list -->

## Page Implementation - CRUD Operations

<!-- page_crud -->
```typescript
import React, { useState } from 'react';
{% if uses_form -%}
import {{ form_component }} from '../components/{{ form_component }}';
{% endif -%}
{% if uses_list -%}
import {{ list_component }} from '../components/{{ list_component }}';
{% endif -%}

const {{ page_name }}Page = () => {
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
    <div className="{{ page_name_lower }}-page">
      <div className="page-header">
        <h1>{{ page_title | default(page_name) }}</h1>
        {mode === 'view' && (
          <button className="btn btn-primary" onClick={handleAdd}>
            + Add New
          </button>
        )}
      </div>

      <div className="page-content">
        {mode === 'view' && (
          <{{ list_component }}
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
            <{{ form_component }}
              {% if mode_edit_check %}data={selectedItem}{% endif %}
              onSuccess={handleSuccess}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default {{ page_name }}Page;
```
<!-- /page_crud -->

## Hook Implementation - useAPI

<!-- hook_use_api -->
```typescript
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
```
<!-- /hook_use_api -->
