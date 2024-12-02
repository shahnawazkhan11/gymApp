import { TextInput, ScrollView, Pressable } from 'react-native';
import { Text, View } from '@/components/Themed';
import { useState } from 'react';

export default function TabTwoScreen() {
  const [measurements, setMeasurements] = useState({
    weight: '',
    neck: '',
    shoulders: '',
    leftBicep: '',
    rightBicep: '',
    leftTricep: '',
    rightTricep: '',
    leftForearm: '',
    rightForearm: '',
    upperAbs: '',
    waist: '',
    hips: '',
    leftCalf: '',
    rightCalf: '',
    leftThigh: '',
    rightThigh: '',
  });

  const handleSubmit = () => {
    // Handle optional fields here
    console.log('Submitting measurements:', measurements);
    // Add your API call here
  };

  return (
    <ScrollView className="flex-1 p-5">
      <Text className="text-2xl font-bold mb-5">Body Measurements</Text>
      
      <TextInput 
        key="weight-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Weight (kg)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.weight}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, weight: text }))}
      />
      <TextInput 
        key="neck-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Neck (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.neck}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, neck: text }))}
      />
      <TextInput 
        key="shoulders-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Shoulders (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.shoulders}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, shoulders: text }))}
      />
      <TextInput 
        key="leftBicep-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Left Bicep (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.leftBicep}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, leftBicep: text }))}
      />
      <TextInput 
        key="rightBicep-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Right Bicep (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.rightBicep}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, rightBicep: text }))}
      />
      <TextInput 
        key="leftTricep-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Left Tricep (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.leftTricep}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, leftTricep: text }))}
      />
      <TextInput 
        key="rightTricep-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Right Tricep (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.rightTricep}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, rightTricep: text }))}
      />
      <TextInput 
        key="leftForearm-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Left Forearm (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.leftForearm}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, leftForearm: text }))}
      />
      <TextInput 
        key="rightForearm-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Right Forearm (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.rightForearm}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, rightForearm: text }))}
      />
      <TextInput 
        key="upperAbs-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Upper Abs (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.upperAbs}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, upperAbs: text }))}
      />
      <TextInput 
        key="waist-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Waist (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.waist}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, waist: text }))}
      />
      <TextInput 
        key="hips-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Hips (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.hips}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, hips: text }))}
      />
      <TextInput 
        key="leftCalf-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Left Calf (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.leftCalf}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, leftCalf: text }))}
      />
      <TextInput 
        key="rightCalf-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Right Calf (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.rightCalf}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, rightCalf: text }))}
      />
      <TextInput 
        key="leftThigh-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Left Thigh (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.leftThigh}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, leftThigh: text }))}
      />
      <TextInput 
        key="rightThigh-input"
        className="h-10 border border-gray-300 mb-2 px-3 rounded text-sm" 
        placeholder="Right Thigh (inches)" 
        placeholderTextColor="#888" 
        keyboardType="numeric"
        value={measurements.rightThigh}
        onChangeText={(text) => setMeasurements(prev => ({ ...prev, rightThigh: text }))}
      />

      <Pressable 
        key="submit-button"
        className="bg-blue-500 p-4 rounded-lg mt-4"
        onPress={handleSubmit}
      >
        <Text className="text-white text-center font-bold">Submit Measurements</Text>
      </Pressable>
    </ScrollView>
  );
}