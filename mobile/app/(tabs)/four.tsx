import React, { useState } from 'react';
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
  id: string;
  name: string;
  exercises: Exercise[];
}

const WorkoutScreen = () => {
  const [selectedTemplate, setSelectedTemplate] = useState<string>('');
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [workoutStarted, setWorkoutStarted] = useState(false);
  const [selectedExercise, setSelectedExercise] = useState('');

  // Predefined templates
  const templates: Template[] = [
    {
      id: '1',
      name: 'Push Day',
      exercises: [
        { name: 'Bench Press', equipment: 'Barbell', sets: [{ previous: '', kg: '', reps: '10', confirmed: false }] },
        { name: 'Shoulder Press', equipment: 'Dumbbell', sets: [{ previous: '', kg: '', reps: '10', confirmed: false }] },
      ]
    },
    {
      id: '2',
      name: 'Pull Day',
      exercises: [
        { name: 'Lateral Raise', equipment: 'Dumbbell', sets: [{ previous: '', kg: '', reps: '10', confirmed: false }] },
        { name: 'Skullcrusher', equipment: 'Barbell', sets: [{ previous: '', kg: '', reps: '10', confirmed: false }] },
      ]
    },
  ];

  const exerciseOptions = [
    { label: 'Lateral Raise (Dumbbell)', value: 'Lateral Raise', equipment: 'Dumbbell' },
    { label: 'Skullcrusher (Barbell)', value: 'Skullcrusher', equipment: 'Barbell' },
    { label: 'Bench Press (Barbell)', value: 'Bench Press', equipment: 'Barbell' },
    { label: 'Shoulder Press (Dumbbell)', value: 'Shoulder Press', equipment: 'Dumbbell' },
  ];

  const handleTemplateSelect = (templateId: string) => {
    const template = templates.find(t => t.id === templateId);
    if (template) {
      setSelectedTemplate(templateId);
      setExercises(template.exercises);
    }
  };

  const addExercise = () => {
    if (!selectedExercise) return;
    
    const exerciseExists = exercises.some(ex => ex.name === selectedExercise);
    if (exerciseExists) {
      Alert.alert('Exercise already added');
      return;
    }

    const selectedOption = exerciseOptions.find(opt => opt.value === selectedExercise);
    if (selectedOption) {
      setExercises([...exercises, {
        name: selectedOption.value,
        equipment: selectedOption.equipment,
        sets: [{ previous: '', kg: '', reps: '10', confirmed: false }]
      }]);
    }
    setSelectedExercise('');
  };

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

  const finishWorkout = () => {
    // Add logic to save workout data
    Alert.alert('Workout Completed', 'Your workout has been saved!');
    setWorkoutStarted(false);
    setExercises([]);
    setSelectedTemplate('');
  };

  return (
    <ScrollView className="flex-1 bg-white">
      <View className="p-4">
        {!workoutStarted ? (
          <View>
            <Text className="text-xl font-bold mb-4">Select Workout Template</Text>
            <Dropdown
              data={templates.map(template => ({ label: template.name, value: template.id }))}
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