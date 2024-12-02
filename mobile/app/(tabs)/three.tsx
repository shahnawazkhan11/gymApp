import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

interface NutritionGoals {
  calories: number;
  water: number; // in ml
  protein: number; // in grams
}

interface NutritionProgress extends NutritionGoals {
  remaining: NutritionGoals;
}

export default function NutritionTracker() {
  const [showGoalInput, setShowGoalInput] = useState(true);
  const [goals, setGoals] = useState<NutritionGoals>({
    calories: 0,
    water: 0,
    protein: 0,
  });
  
  const [progress, setProgress] = useState<NutritionProgress>({
    calories: 0,
    water: 0,
    protein: 0,
    remaining: {
      calories: 0,
      water: 0,
      protein: 0,
    },
  });

  const [intakeInput, setIntakeInput] = useState({
    calories: '',
    water: '',
    protein: '',
  });

  const handleSetGoals = () => {
    setShowGoalInput(false);
    setProgress(prev => ({
      ...prev,
      remaining: goals,
    }));
  };

  const handleIntake = () => {
    const caloriesNum = Number(intakeInput.calories || 0);
    const waterNum = Number(intakeInput.water || 0);
    const proteinNum = Number(intakeInput.protein || 0);

    setProgress(prev => ({
      ...prev,
      calories: prev.calories + caloriesNum,
      water: prev.water + waterNum,
      protein: prev.protein + proteinNum,
      remaining: {
        calories: goals.calories - (prev.calories + caloriesNum),
        water: goals.water - (prev.water + waterNum),
        protein: goals.protein - (prev.protein + proteinNum),
      }
    }));

    setIntakeInput({ calories: '', water: '', protein: '' });
  };

  return (
    <SafeAreaView className="flex-1 bg-white">
      <ScrollView className="p-4">
        {showGoalInput ? (
          <View className="space-y-4">
            <Text className="text-xl font-bold text-gray-800">Set Daily Goals</Text>
            <View className="space-y-3">
              <View>
                <Text className="text-gray-700 mb-1 font-medium">Daily Calorie Goal</Text>
                <TextInput
                  className="p-2 border border-gray-300 rounded-lg"
                  placeholder="Enter calories (e.g., 2000)"
                  keyboardType="numeric"
                  value={String(goals.calories)}
                  onChangeText={(text) => setGoals(prev => ({ ...prev, calories: Number(text) }))}
                />
              </View>

              <View>
                <Text className="text-gray-700 mb-1 font-medium">Daily Water Goal</Text>
                <TextInput
                  className="p-2 border border-gray-300 rounded-lg"
                  placeholder="Enter water in ml (e.g., 2000)"
                  keyboardType="numeric"
                  value={String(goals.water)}
                  onChangeText={(text) => setGoals(prev => ({ ...prev, water: Number(text) }))}
                />
              </View>

              <View>
                <Text className="text-gray-700 mb-1 font-medium">Daily Protein Goal</Text>
                <TextInput
                  className="p-2 border border-gray-300 rounded-lg"
                  placeholder="Enter protein in grams (e.g., 60)"
                  keyboardType="numeric"
                  value={String(goals.protein)}
                  onChangeText={(text) => setGoals(prev => ({ ...prev, protein: Number(text) }))}
                />
              </View>

              <TouchableOpacity
                className="bg-blue-500 p-3 rounded-lg mt-2"
                onPress={handleSetGoals}
              >
                <Text className="text-white text-center font-bold">Set Goals</Text>
              </TouchableOpacity>
            </View>
          </View>
        ) : (
          <View className="space-y-6">
            <View className="space-y-4">
              <Text className="text-xl font-bold text-gray-800">Track Your Intake</Text>
              <View className="space-y-2">
                <TextInput
                  className="p-2 border border-gray-300 rounded-lg"
                  placeholder="Calories Consumed"
                  keyboardType="numeric"
                  value={intakeInput.calories}
                  onChangeText={(text) => {
                    const filtered = text.replace(/[^0-9]/g, '');
                    setIntakeInput(prev => ({ ...prev, calories: filtered }));
                  }}
                />
                <TextInput
                  className="p-2 border border-gray-300 rounded-lg"
                  placeholder="Water Consumed (ml)"
                  keyboardType="numeric"
                  value={intakeInput.water}
                  onChangeText={(text) => {
                    const filtered = text.replace(/[^0-9]/g, '');
                    setIntakeInput(prev => ({ ...prev, water: filtered }));
                  }}
                />
                <TextInput
                  className="p-2 border border-gray-300 rounded-lg"
                  placeholder="Protein Consumed (g)"
                  keyboardType="numeric"
                  value={intakeInput.protein}
                  onChangeText={(text) => {
                    const filtered = text.replace(/[^0-9]/g, '');
                    setIntakeInput(prev => ({ ...prev, protein: filtered }));
                  }}
                />
                <TouchableOpacity
                  className="bg-green-500 p-3 rounded-lg"
                  onPress={handleIntake}
                  activeOpacity={0.7}
                >
                  <Text className="text-white text-center font-bold">Add Intake</Text>
                </TouchableOpacity>
              </View>
            </View>

            <View className="space-y-4">
              <Text className="text-xl font-bold text-gray-800">Progress</Text>
              <View className="space-y-2">
                {/* Calories Progress */}
                <View key="calories-progress" className="bg-gray-100 p-4 rounded-lg">
                  {progress.remaining.calories <= 0 ? (
                    <Text className="text-green-600 font-bold">Calorie goal completed! 🎉</Text>
                  ) : (
                    <Text className="text-gray-800">Calories: {progress.remaining.calories} remaining</Text>
                  )}
                  <View className="w-full bg-gray-200 h-2 rounded-full mt-2">
                    <View 
                      className={`h-2 rounded-full ${progress.remaining.calories <= 0 ? 'bg-green-500' : 'bg-blue-500'}`}
                      style={{ width: `${Math.min((progress.calories / goals.calories) * 100, 100)}%` }}
                    />
                  </View>
                </View>

                {/* Water Progress */}
                <View key="water-progress" className="bg-gray-100 p-4 rounded-lg">
                  {progress.remaining.water <= 0 ? (
                    <Text className="text-green-600 font-bold">Water goal completed! 🎉</Text>
                  ) : (
                    <Text className="text-gray-800">Water: {progress.remaining.water}ml remaining</Text>
                  )}
                  <View className="w-full bg-gray-200 h-2 rounded-full mt-2">
                    <View 
                      className={`h-2 rounded-full ${progress.remaining.water <= 0 ? 'bg-green-500' : 'bg-blue-500'}`}
                      style={{ width: `${Math.min((progress.water / goals.water) * 100, 100)}%` }}
                    />
                  </View>
                </View>

                {/* Protein Progress */}
                <View key="protein-progress" className="bg-gray-100 p-4 rounded-lg">
                  {progress.remaining.protein <= 0 ? (
                    <Text className="text-green-600 font-bold">Protein goal completed! 🎉</Text>
                  ) : (
                    <Text className="text-gray-800">Protein: {progress.remaining.protein}g remaining</Text>
                  )}
                  <View className="w-full bg-gray-200 h-2 rounded-full mt-2">
                    <View 
                      className={`h-2 rounded-full ${progress.remaining.protein <= 0 ? 'bg-green-500' : 'bg-blue-500'}`}
                      style={{ width: `${Math.min((progress.protein / goals.protein) * 100, 100)}%` }}
                    />
                  </View>
                </View>
              </View>
            </View>

            <TouchableOpacity
              className="bg-gray-500 p-3 rounded-lg"
              onPress={() => setShowGoalInput(true)}
            >
              <Text className="text-white text-center font-bold">Reset Goals</Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}
