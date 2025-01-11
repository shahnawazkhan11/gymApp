declare module '../../services/api' {
    export const exerciseApi: {
        getTemplates: () => Promise<{ data: any[] }>;
        createWorkoutRecord: (data: { template_id: number; start_time: string }) => Promise<void>;
        fetchExercises: () => Promise<{ data: any[] }>;
        // Add other methods as needed
    };
} 