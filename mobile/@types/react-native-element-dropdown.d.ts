declare module 'react-native-element-dropdown' {
    import { Component } from 'react';
    import { ViewStyle, TextStyle } from 'react-native';

    export interface DropdownProps {
        data: Array<{ label: string; value: any }>;
        labelField?: string;
        valueField?: string;
        placeholder?: string;
        value?: any;
        onChange?: (item: any) => void;
        style?: ViewStyle;
        placeholderStyle?: TextStyle;
        // Add other props as needed
    }

    export class Dropdown extends Component<DropdownProps> {}
} 