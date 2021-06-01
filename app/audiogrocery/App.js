/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

import React from 'react';
import { StyleSheet, Text, View, TouchableHighlight } from 'react-native';
import axios from 'axios';
import Voice from 'react-native-voice';
import Tts from 'react-native-tts';
import type {Node} from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  useColorScheme,
  View,
} from 'react-native';

import {
  Colors,
  DebugInstructions,
  Header,
  LearnMoreLinks,
  ReloadInstructions,
} from 'react-native/Libraries/NewAppScreen';

const _backendEndpoint = '<YOUR_ORCHESTRATOR_URL>';

/** Constructor Component to Set Language and Voice Handler **/
constructor(props) {
  super(props);

  this.state = {
    text: '',
    status: '',
    userPayload: '',
    userSession: ''
  }

  Voice.onSpeechStart = this.onSpeechStartHandler
  Voice.onSpeechEnd = this.onSpeechEndHandler
  Voice.onSpeechResults = this.onSpeechResultsHandler
  Tts.setDefaultLanguage('en-US');
}

 /**
 * send message to API
 */
sendMessage = async payload => {
  try {
    let { userSession } = this.state;
    let inputPayload = {
      input: {
        message_type: "text",
        text: payload
      }
    }

    let responseData = { ...inputPayload, ...userSession }
    let response = await axios.post(`http://127.0.0.1:8080/speech/en`, responseData)
    this.setState({ text: response.data.output.generic[0].text });
    Tts.speak(response.data.output.generic[0].text);
  }
  catch (err) { console.log('Failed to send data to Watson API', err) }
}

const Section = ({children, title}): Node => {
  const isDarkMode = useColorScheme() === 'dark';
  return (
    <View style={styles.sectionContainer}>
      <Text
        style={[
          styles.sectionTitle,
          {
            color: isDarkMode ? Colors.white : Colors.black,
          },
        ]}>
        {title}
      </Text>
      <Text
        style={[
          styles.sectionDescription,
          {
            color: isDarkMode ? Colors.light : Colors.dark,
          },
        ]}>
        {children}
      </Text>
    </View>
  );
};

 // Handle voice capture event
 onSpeechResultsHandler = result => {
  this.setState({ text: result.value[0] });
  this.sendMessage(result.value[0]);
}

// Listening to start
onSpeechStartHandler = () => {
  this.setState({ status: 'Listening...' });
}

// Listening to end
onSpeechEndHandler = () => {
  this.setState({ status: 'Voice Processed' });
}

// Listening to press button to speak
onStartButtonPress = e => {
  Voice.start('pt-BR');
}

// Listening to release button to speak
onStopButtonPress = e => {
  Voice.stop();
  Tts.stop();
}

const App: () => Node = () => {
  const isDarkMode = useColorScheme() === 'dark';

  const backgroundStyle = {
    backgroundColor: isDarkMode ? Colors.darker : Colors.lighter,
  };

  return (
    <SafeAreaView style={backgroundStyle}>
      <StatusBar barStyle={isDarkMode ? 'light-content' : 'dark-content'} />
      <ScrollView
        contentInsetAdjustmentBehavior="automatic"
        style={backgroundStyle}>
        <Header />
        <View
          style={{
            backgroundColor: isDarkMode ? Colors.black : Colors.white,
          }}>
          <Section title="Step One">
            Edit <Text style={styles.highlight}>App.js</Text> to change this
            screen and then come back to see your edits.
          </Section>
          <Section title="See Your Changes">
            <ReloadInstructions />
          </Section>
          <Section title="Debug">
            <DebugInstructions />
          </Section>
          <Section title="Learn More">
            Read the docs to discover what to do next:
          </Section>
          <LearnMoreLinks />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  sectionContainer: {
    marginTop: 32,
    paddingHorizontal: 24,
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: '600',
  },
  sectionDescription: {
    marginTop: 8,
    fontSize: 18,
    fontWeight: '400',
  },
  highlight: {
    fontWeight: '700',
  },
});

export default App;
