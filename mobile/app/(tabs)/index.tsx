import { ScrollView, Text, View, Pressable } from 'react-native';

type Exercise = {
  id: string;
  name: string;
  category: string;
};

const recentExercises: Exercise[] = [
  {
    id: '1',
    name: 'Hanging Knee Raise',
    category: 'Core',
  },
  {
    id: '2',
    name: "Knee Raise (Captain's Chair)",
    category: 'Core',
  },
  {
    id: '3',
    name: 'Plank',
    category: 'Core',
  },
  {
    id: '4',
    name: 'Sit-up',
    category: 'Core',
  },
];

export default function TabOneScreen() {
  return (
    <View className="flex-1 bg-white">
      <View className="px-6 pt-4">
        <Text className="text-4xl font-bold mb-6">Exercises</Text>
        <Text className="text-gray-500 text-lg mb-4">RECENT</Text>
      </View>
      
      <ScrollView className="flex-1 px-6">
        {recentExercises.map((exercise) => (
          <Pressable 
            key={exercise.id}
            className="flex-row items-center py-3"
          >
            <View>
              <Text className="text-lg font-semibold">{exercise.name}</Text>
              <Text className="text-gray-500">{exercise.category}</Text>
            </View>
          </Pressable>
        ))}
      </ScrollView>
    </View>
  );
}