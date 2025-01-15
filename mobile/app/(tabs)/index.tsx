import { ScrollView, Text, View, Pressable } from 'react-native';
import React, { useEffect, useState } from 'react';

type Exercise = {
  id: string;
  name: string;
  description: string;
  bodypart: string;
  equipment: string;
  difficulty: string;
  tags: string[];
  created_at: string;
  updated_at: string;
};

export default function TabOneScreen() {
  const [recentExercises, setRecentExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchExercises = async () => {
      try {
        const response = await fetch('http://10.0.2.2:8000/api/exercises/');
        if (!response.ok) {
          throw new Error('Failed to fetch exercises');
        }
        const data = await response.json();
        console.log('Fetched exercises:', data);
        setRecentExercises(data.results); // Use the results array
      } catch (error) {
        console.error('Error fetching exercises:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
  
    fetchExercises();
  }, []);
  

  if (loading) {
    return <Text>Loading...</Text>;
  }

  if (error) {
    return <Text>Error: {error}</Text>;
  }

  if (recentExercises.length === 0) {
    return <Text>No exercises available.</Text>;
  }

  return (
    <View className="flex-1 bg-white">
      <View className="px-6 pt-4">
        <Text className="text-4xl font-bold mb-6">Exercises</Text>
        <Text className="text-gray-500 text-lg mb-4">RECENT</Text>
      </View>
      
      <ScrollView className="flex-1 px-6">
  {recentExercises.map((Exercise) => (
    <Pressable 
      key={Exercise.id}
      className="flex-row items-center py-3"
    >
      <View>
        <Text className="text-lg font-semibold">{Exercise.name}</Text>
        <Text className="text-gray-500">{Exercise.bodypart}</Text>
        <Text className="text-gray-500">{Exercise.equipment}</Text>
      </View>
    </Pressable>
  ))}
</ScrollView>
    </View>
  );
}