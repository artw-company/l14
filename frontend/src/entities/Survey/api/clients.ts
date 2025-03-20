import { axiosInstance } from '@/app/api';
import type { Survey } from '@/entities/Survey';

export const SurveyClient = {
  get: (id: Survey['id']) => axiosInstance.get<Survey>(`/survey/${id}/`),
  put: (id: Survey['id'], survey: Survey) => axiosInstance.put(`/survey/${id}/`, survey),
};
