import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, TextInput, ScrollView, Alert } from 'react-native';
import { Dropdown } from 'react-native-element-dropdown';

interface Set {
  previous: string;
  kg: string;
  reps: string;
  confirmed: boolean;
}

interface Exercise {
  name: string;
  sets: Set[];
  equipment: string;
}

interface Template {
  id: number;
  name: string;
  exercises: number[];
}

interface APIExercise {
  id: number;
  name: string;
  equipment: string;
  description: string;
  bodypart: string;
  difficulty: string;
  tags: string[];
}

const WorkoutScreen = () => {
  const [selectedTemplate, setSelectedTemplate] = useState<string>('');
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [workoutStarted, setWorkoutStarted] = useState(false);
  const [selectedExercise, setSelectedExercise] = useState('');
  const [templates, setTemplates] = useState<Template[]>([]);
  const [availableExercises, setAvailableExercises] = useState<APIExercise[]>([]);

  // Fetch exercises from API
  const fetchExercises = async () => {
    try {
      const response = await fetch('http://10.0.2.2:8000/api/exercises/');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setAvailableExercises(data.results);
    } catch (error) {
      console.error('Error fetching exercises:', error);
    }
  };

  // Fetch templates from API
  const fetchTemplates = async () => {
    try {
      const response = await fetch('http://10.0.2.2:8000/api/templates/');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setTemplates(data.results);
    } catch (error) {
      console.error('Error fetching templates:', error);
    }
  };

  useEffect(() => {
    fetchExercises();
    fetchTemplates();
  }, []);

  // Convert API exercises to dropdown format
  const exerciseOptions = availableExercises.map(exercise => ({
    label: `${exercise.name} (${exercise.equipment})`,
    value: exercise.id.toString(),
    equipment: exercise.equipment
  }));

  const handleTemplateSelect = (templateId: string) => {
    const template = templates.find(t => t.id.toString() === templateId);
    if (template) {
      setSelectedTemplate(templateId);
      
      // Convert template exercise IDs to full exercise objects
      const templateExercises = template.exercises.map(exerciseId => {
        const apiExercise = availableExercises.find(ex => ex.id === exerciseId);
        if (apiExercise) {
          return {
            name: apiExercise.name,
            equipment: apiExercise.equipment,
            sets: [{ previous: '', kg: '', reps: '10', confirmed: false }]
          };
        }
        return null;
      }).filter((ex): ex is Exercise => ex !== null);

      setExercises(templateExercises);
    }
  };

  const addExercise = () => {
    if (!selectedExercise) return;
    
    const exerciseExists = exercises.some(ex => ex.name === selectedExercise);
    if (exerciseExists) {
      Alert.alert('Exercise already added');
      return;
    }

    const selectedApiExercise = availableExercises.find(ex => ex.id.toString() === selectedExercise);
    if (selectedApiExercise) {
      setExercises([...exercises, {
        name: selectedApiExercise.name,
        equipment: selectedApiExercise.equipment,
        sets: [{ previous: '', kg: '', reps: '10', confirmed: false }]
      }]);
    }
    setSelectedExercise('');
  };

  // Rest of the component remains the same
  const addSet = (exerciseIndex: number) => {
    const updatedExercises = [...exercises];
    const lastSet = updatedExercises[exerciseIndex].sets[updatedExercises[exerciseIndex].sets.length - 1];
    updatedExercises[exerciseIndex].sets.push({
      previous: '',
      kg: lastSet?.kg || '',
      reps: '10',
      confirmed: false
    });
    setExercises(updatedExercises);
  };

  const updateSet = (exerciseIndex: number, setIndex: number, field: keyof Set, value: string | boolean) => {
    const updatedExercises = [...exercises];
    updatedExercises[exerciseIndex].sets[setIndex][field] = value;
    setExercises(updatedExercises);
  };

  const removeExercise = (index: number) => {
    setExercises(exercises.filter((_, i) => i !== index));
  };

  const finishWorkout = async () => {
    try {
      // First, let's log what we're sending
      const workoutData = {
        template: selectedTemplate ? parseInt(selectedTemplate) : null,
        workout_exercises: exercises.map((exercise, index) => ({
          exercise: availableExercises.find(ex => ex.name === exercise.name)?.id,
          order: index,
          workout_sets: exercise.sets.map((set, setIndex) => ({
            weight: parseFloat(set.kg) || 0,
            reps: parseInt(set.reps) || 0,
            completed: set.confirmed,
            order: setIndex
          }))
        }))
      };
  
      console.log('Sending workout data:', JSON.stringify(workoutData, null, 2));
  
      const response = await fetch('http://10.0.2.2:8000/api/workouts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(workoutData)
      });
  
      // Log the full response
      const responseData = await response.json();
      console.log('Response status:', response.status);
      console.log('Response data:', responseData);
  
      if (!response.ok) {
        throw new Error(JSON.stringify(responseData) || 'Failed to save workout');
      }
  
      Alert.alert('Success', 'Workout saved successfully!');
      setWorkoutStarted(false);
      setExercises([]);
      setSelectedTemplate('');
  
    } catch (error) {
      console.error('Full error:', error);
      // Show more detailed error message
      Alert.alert(
        'Error', 
        typeof error.message === 'string' ? error.message : 'Failed to save workout. Check console for details.'
      );
    }
  };
      
  return (
    <ScrollView className="flex-1 bg-white">
      <View className="p-4">
        {!workoutStarted ? (
          <View>
            <Text className="text-xl font-bold mb-4">Select Workout Template</Text>
            <Dropdown
              data={templates.map(template => ({ label: template.name, value: template.id.toString() }))}
              labelField="label"
              valueField="value"
              placeholder="Select Template"
              value={selectedTemplate}
              onChange={item => handleTemplateSelect(item.value)}
              className="border border-gray-300 rounded-md p-2 mb-4"
            />
            
            {selectedTemplate && (
              <View>
                <Text className="text-lg font-semibold mb-2">Exercises in template:</Text>
                {exercises.map((exercise, index) => (
                  <Text key={index} className="mb-1">• {exercise.name} ({exercise.equipment})</Text>
                ))}
                
                <TouchableOpacity 
                  onPress={() => setWorkoutStarted(true)}
                  className="bg-green-500 p-3 rounded-md mt-4"
                >
                  <Text className="text-white text-center">Start Workout</Text>
                </TouchableOpacity>
              </View>
            )}
          </View>
        ) : (
          <View>
            <View className="flex-row justify-between items-center mb-4">
              <Text className="text-xl font-bold">Current Workout</Text>
              <TouchableOpacity onPress={finishWorkout}>
                <Text className="text-blue-500 font-semibold">FINISH</Text>
              </TouchableOpacity>
            </View>

            <Dropdown
              data={exerciseOptions}
              labelField="label"
              valueField="value"
              placeholder="Add Exercise"
              value={selectedExercise}
              onChange={item => setSelectedExercise(item.value)}
              className="border border-gray-300 rounded-md p-2 mb-4"
            />
            
            <TouchableOpacity 
              onPress={addExercise}
              className="bg-blue-500 p-3 rounded-md mb-4"
            >
              <Text className="text-white text-center">Add Exercise</Text>
            </TouchableOpacity>

            {exercises.map((exercise, exerciseIndex) => (
              <View key={exerciseIndex} className="mb-6">
                <View className="flex-row justify-between items-center mb-2">
                  <Text className="text-lg font-bold">{exercise.name} ({exercise.equipment})</Text>
                  <TouchableOpacity onPress={() => removeExercise(exerciseIndex)}>
                    <Text className="text-red-500">Remove</Text>
                  </TouchableOpacity>
                </View>

                <View className="mb-2">
                  <View className="flex-row justify-between mb-2">
                    <Text className="w-10">SET</Text>
                    <Text className="w-24">PREVIOUS</Text>
                    <Text className="w-16">KG</Text>
                    <Text className="w-16">REPS</Text>
                    <Text className="w-20">CONFIRM</Text>
                  </View>

                  {exercise.sets.map((set, setIndex) => (
                    <View key={setIndex} className="flex-row justify-between items-center mb-2">
                      <Text className="w-10">{setIndex + 1}</Text>
                      <Text className="w-24">{set.previous || '-'}</Text>
                      <TextInput
                        value={set.kg}
                        onChangeText={(value) => updateSet(exerciseIndex, setIndex, 'kg', value)}
                        className="border w-16 p-1 text-center"
                        keyboardType="numeric"
                      />
                      <TextInput
                        value={set.reps}
                        onChangeText={(value) => updateSet(exerciseIndex, setIndex, 'reps', value)}
                        className="border w-16 p-1 text-center"
                        keyboardType="numeric"
                      />
                      <TouchableOpacity 
                        onPress={() => updateSet(exerciseIndex, setIndex, 'confirmed', !set.confirmed)}
                        className="w-20"
                      >
                        <Text className={set.confirmed ? "text-green-500" : "text-gray-400"}>
                          {set.confirmed ? "✓" : "○"}
                        </Text>
                      </TouchableOpacity>
                    </View>
                  ))}
                </View>

                <TouchableOpacity 
                  onPress={() => addSet(exerciseIndex)}
                  className="bg-blue-500 p-2 rounded-md"
                >
                  <Text className="text-white text-center">Add Set</Text>
                </TouchableOpacity>
              </View>
            ))}

            <TouchableOpacity 
              onPress={() => {
                setWorkoutStarted(false);
                setExercises([]);
                setSelectedTemplate('');
              }}
              className="bg-red-500 p-3 rounded-md mt-4"
            >
              <Text className="text-white text-center">Cancel Workout</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>
    </ScrollView>
  );
};

export default WorkoutScreen;