import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, Dimensions } from 'react-native';
import { LineChart } from 'react-native-chart-kit';

const WorkoutCharts = () => {
  const [chartData, setChartData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchWorkoutData();
  }, []);

  const validateNumber = (value) => {
    const num = parseFloat(value);
    return !isNaN(num) && isFinite(num) ? num : 0;
  };

  const fetchWorkoutData = async () => {
    try {
      const response = await fetch('http://10.0.2.2:8000/api/workouts/');
      const data = await response.json();
      
      // Process the data for charts
      const processedData = {};
      
      data.results.forEach(workout => {
        workout.workout_exercises.forEach(exercise => {
          const exerciseName = exercise.exercise_detail.name;
          
          if (!processedData[exerciseName]) {
            processedData[exerciseName] = {
              sets: [],
              reps: [],
              weights: [],
              dates: []
            };
          }
          
          exercise.workout_sets.forEach((set, setIndex) => {
            if (set.completed) {
              // Validate and clean the data
              const weight = validateNumber(set.weight);
              const reps = validateNumber(set.reps);
              
              if (weight >= 0 && reps >= 0) {
                processedData[exerciseName].sets.push(setIndex + 1);
                processedData[exerciseName].reps.push(reps);
                processedData[exerciseName].weights.push(weight);
                processedData[exerciseName].dates.push(new Date(workout.date).toLocaleDateString());
              }
            }
          });
        });
      });

      // Filter out exercises with no valid data
      const cleanedData = Object.entries(processedData).reduce((acc, [name, data]) => {
        if (data.sets.length > 0) {
          acc[name] = data;
        }
        return acc;
      }, {});
      
      setChartData(cleanedData);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching workout data:', error);
      setError('Failed to load workout data');
      setLoading(false);
    }
  };

  const chartConfig = {
    backgroundColor: '#ffffff',
    backgroundGradientFrom: '#ffffff',
    backgroundGradientTo: '#ffffff',
    decimalPlaces: 0,
    color: (opacity = 1) => `rgba(0, 100, 255, ${opacity})`,
    style: {
      borderRadius: 16,
    },
  };

  const screenWidth = Dimensions.get('window').width - 32;

  if (loading) {
    return (
      <View className="flex-1 justify-center items-center">
        <Text>Loading...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View className="flex-1 justify-center items-center">
        <Text className="text-red-500">{error}</Text>
      </View>
    );
  }

  if (Object.keys(chartData).length === 0) {
    return (
      <View className="flex-1 justify-center items-center">
        <Text>No workout data available</Text>
      </View>
    );
  }

  return (
    <ScrollView className="flex-1 bg-white px-4">
      {Object.entries(chartData).map(([exerciseName, data]) => (
        <View key={exerciseName} className="mb-8">
          <Text className="text-xl font-bold mb-4">{exerciseName}</Text>
          
          {/* Sets vs Reps Chart */}
          {data.reps.length > 0 && (
            <View className="mb-6 p-4 bg-gray-50 rounded-lg">
              <Text className="text-lg font-semibold mb-2">Sets vs Reps</Text>
              <LineChart
                data={{
                  labels: data.sets.map(String),
                  datasets: [{
                    data: data.reps
                  }]
                }}
                width={screenWidth}
                height={220}
                chartConfig={chartConfig}
                bezier
                style={{
                  marginVertical: 8,
                  borderRadius: 16,
                }}
                yAxisLabel=""
                yAxisSuffix=" reps"
                xAxisLabel="Set "
              />
            </View>
          )}

          {/* Sets vs Weights Chart */}
          {data.weights.length > 0 && (
            <View className="p-4 bg-gray-50 rounded-lg">
              <Text className="text-lg font-semibold mb-2">Sets vs Weight</Text>
              <LineChart
                data={{
                  labels: data.sets.map(String),
                  datasets: [{
                    data: data.weights
                  }]
                }}
                width={screenWidth}
                height={220}
                chartConfig={chartConfig}
                bezier
                style={{
                  marginVertical: 8,
                  borderRadius: 16,
                }}
                yAxisLabel=""
                yAxisSuffix=" kg"
                xAxisLabel="Set "
              />
            </View>
          )}

          {/* Date Information */}
          <Text className="text-sm text-gray-500 mt-2">
            Data from: {data.dates.join(', ')}
          </Text>
        </View>
      ))}
    </ScrollView>
  );
};

export default WorkoutCharts;