/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useState, useContext} from 'react';
import {View, Text} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {Container, HeaderButton} from '../../Components';
import useAppTheme from '../../Themes/Context';
import {IconX, ICON_TYPE} from '../../Icons';
import {TouchableOpacity} from 'react-native';
import {ButtonX} from '../../Components';
import AudioRecord from 'react-native-audio-record';
import {BASE_URL} from '../../Config/index';
import Tts from 'react-native-tts';
// import { Voice } from 'react-native-voice';
import AsyncStorage from '@react-native-community/async-storage';
import en from '../../en.json';
import ta from '../../ta.json';
import {LocalizationContext} from '../../Translations';
import { Voice } from '@react-native-voice/voice';

const MainScreen = ({routes, navigation}) => {
  const {theme} = useAppTheme();
  const [language, setLanguage] = useState('en');
  const [languageTts, setLanguageTts] = useState('en-IN');
  const [locale, setLocale] = useState('en_us');
  const [isRecording, setIsRecording] = useState(false);

  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"

  const {
    translations,
  } = useContext(LocalizationContext);


  // eslint-disable-next-line prettier/prettier
  useEffect(() => {
    Voice.onSpeechStart = onSpeechStart()
    Voice.onSpeechRecognized = onSpeechRecognized()
    Voice.onSpeechResults = onSpeechResults()

    // Load the Chosen Language
    console.log(appLanguage)

    if (language == 'ta') {
      setLanguage('ta')
      setLanguageTts('ta-IN')
    } else {
      setLanguage('en')
      setLanguageTts('en-IN')
    }

    const anew = '2.2';
    var myNumber = 120.2;
    var myString = myNumber.toString();

    Tts.speak(translations['menuSelectionTts'], {
      androidParams: {
        KEY_PARAM_PAN: -1,
        KEY_PARAM_VOLUME: 0.5,
        KEY_PARAM_STREAM: 'STREAM_MUSIC',
      },
    });

    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };

    AudioRecord.init(options);
    const _toggleDrawer = () => {
      navigation.toggleDrawer();
    };

    const interval = setInterval(() => {
      if (!isRecording) {
        // Not Recording username or password
        Voice.stop() // Stop Recording
        Voice.start(locale) // Start Recording Again
      }
    }, 5000);
  
    return () => clearInterval(interval); // This represents the unmount function, in which you need to clear your interval to prevent memory leaks.
  }, [navigation, theme.colors.headerTitle]);

  const onSpeechStart = (e) => {

  }

  const onSpeechRecognized = (e) => {
    
  }

  const onSpeechResults = (e) => {
    if (isRecording == false) {
      if (e.value.includes(LISTEN_COMMAND_EN) || e.value.includes(LISTEN_COMMAND_TA)) {
        setIsRecording(true)
        Voice.start(locale)
      }
    } else {
      // Read the Voice Result
      console.log(e.value)
      var menuitem = e.value;
      if (menuitem.includes("voice search") || menuitem.includes("குரல் தேடல்")) {
        navigation.navigate('voiceSearch')
      } else if (menuitem.includes("image search") || menuitem.includes("பட தேடல்")) {
        navigation.navigate('imageSearch')
      } else if (menuitem.includes("product list search") || menuitem.includes("தயாரிப்பு பட்டியல் தேடல்")) {
        navigation.navigate('create-list')
      } else if (menuitem.includes("profile") || menuitem.includes("சுயவிவரம்")) {
        navigation.navigate('profile')
      } else if (menuitem.includes("order") || menuitem.includes("ஒர்டெர்")) {
        navigation.navigate('orderMenu')
      } else if (menuitem.includes("assistant") || menuitem.includes("உதவியாளர்")) {
        navigation.navigate('assistant')
      } else if (menuitem.includes("go back") || menuitem.includes("திரும்பி செல்")) {
        navigation.navigate('assistant');
      }
      
      setIsRecording(false)
    }
  }

  const record = () => {
    console.log('record');

    AudioRecord.start();
    timeout;
    let timeout = setTimeout(() => {
      stopRecord();
      console.log('hello');
    }, 5000);
  };
  
  const stopRecord = async () => {
    console.log('recordStop ');
    const audioFile = await AudioRecord.stop();
    AudioRecord.on('data', (data) => {});
    console.log('audioFile latees 🍷🍷', audioFile);
    initialRec(audioFile);
  };

  const initialRec = (audioFile) => {
    uploadAudio(audioFile);
    console.log('initialRec', audioFile);
    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };
  };

  const uploadAudio = async (fileUrl) => {
    let formData = new FormData();
    formData.append('audioFile', {
      uri: 'file:///data/user/0/com.easy_boiler/files/test.wav',
      type: 'audio/wav',
      name: 'test.wav',
    });

    formData.append('flag', 'name');
    console.log(formData);

    fetch(`${BASE_URL}/navigation/en`, {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((response) => {

        if (!response.flag != 'navigation-error') {
          navigation.navigate(response.flag);
        } else {
          console.log('route error');
        }
      })
      .catch((err) => console.error(err));
  };

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
        }}>
        
        <ButtonX
          accessible={true}
          accessibilityLabel={translations['voiceSearchLabel']}
          accessibilityHint={translations['voiceSearchHint']}
          accessibilityRole="button"
          dark={true}
          color={theme.colors.primary}
          onPress = {() => Tts.speak(translations['voiceSearchLongPress'])}
          onLongPress={() => navigation.navigate('voiceSearch')}
          label={translations['voiceSearchLabel']}
        />
        
        <ButtonX
          accessible={true}
          accessibilityLabel={translations['imageSearchLabel']}
          accessibilityHint={translations['imageSearchHint']}
          accessibilityRole="button"
          dark={true}
          color={theme.colors.primary}
          onPress = {() => Tts.speak(translations['imageSearchLongPress'])}
          onLongPress={() => navigation.navigate('imageSearch')}
          label={translations['imageSearchLabel']}
        />

        <ButtonX
          accessible={true}
          accessibilityLabel={translations['productListSearchLabel']}
          accessibilityHint={translations['productListSearchHint']}
          accessibilityRole="button"
          dark={true}
          color={theme.colors.primary}
          onPress = {() => Tts.speak(translations['productListSearchLongPress'])}
          onPress={() => navigation.navigate('create-list')}
          label={translations['productListSearchLabel']}
        />

        <ButtonX
          accessible={true}
          accessibilityLabel={translations['profileLabel']}
          accessibilityHint={translations['profileHint']}
          accessibilityRole="button"
          dark={true}
          color={theme.colors.primary}
          onPress = {() => Tts.speak(translations['profileLongPress'])}
          onPress={() => navigation.navigate('profile')}
          label={translations['profileLabel']}
        />

        <ButtonX
          accessible={true}
          accessibilityLabel={translations['orderLabel']}
          accessibilityHint={translations['orderHint']}
          accessibilityRole="button"
          dark={true}
          color={theme.colors.primary}
          onPress = {() => Tts.speak(translations['orderLongPress'])}
          onPress={() => navigation.navigate('orderMenu')}
          label={translations['orderLabel']}
        />

        <ButtonX
          accessible={true}
          accessibilityLabel={translations['assistantLabel']}
          accessibilityHint={translations['assistantHint']}
          accessibilityRole="button"
          dark={true}
          color={theme.colors.primary}
          onPress = {() => Tts.speak(translations['assistantLongPress'])}
          onPress={() => navigation.navigate('assistant')}
          label={translations['assistantLabel']}
        />

        <View style={{alignItems: 'center'}}>
          <TouchableOpacity 
            onPress={record}
            accessible={true}
            accessibilityLabel={translations['micMenuLabel']}
            >
            <View
              style={{
                padding: 10,
                marginTop: 20,
                backgroundColor: theme.colors.primary,
                borderRadius: 10,
              }}>
              <IconX name={'md-mic'} style={{color: '#fff'}} />
            </View>
          </TouchableOpacity>
        </View>
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
