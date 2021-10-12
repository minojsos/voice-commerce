/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useContext, useState} from 'react';
import {View, Text} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {Container, HeaderButton} from '../../Components';
import useAppTheme from '../../Themes/Context';
import {IconX, ICON_TYPE} from '../../Icons';
import {Image} from 'react-native';
import metrics from '../../Themes/Metrics';
import {useStoreState} from 'easy-peasy';
import Fonts from '../../Themes/Fonts';
import {TouchableOpacity} from 'react-native';
import NavigationService from '../../Navigation/index';
import Routes from '../../Navigation/Routes/index';
import AudioRecord from 'react-native-audio-record';
import {BASE_URL} from '../../Config/index';
import AsyncStorage from '@react-native-community/async-storage';
import {Section, PasswordInputX, InputX, ButtonX} from '../../Components';
import Tts from 'react-native-tts';
import en from '../../en.json';
import ta from '../../ta.json';
import {LocalizationContext} from '../../Translations';

const MainScreen = ({routes, navigation}) => {
  const {theme} = useAppTheme();

  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));

  const {
    translations
  } = useContext(LocalizationContext);

  Tts.speak(translations['chooseLanguageAudio']);

  useEffect(() => {
    const _toggleDrawer = () => {
      navigation.toggleDrawer();
    };
    // await AsyncStorage.setItem('userId', 1)
    
    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };

    AudioRecord.init(options);

    console.log('use effect home');

    navigation.setOptions({
      headerLeft: () => {
        return (
          <View style={{marginLeft: 10}}>
            <HeaderButton
              icon="menuunfold"
              color={theme.colors.headerTitle}
              iconOrigin={ICON_TYPE.ANT_ICON}
              onPress={_toggleDrawer}
            />
          </View>
        );
      },
    });
  }, [navigation, theme.colors.headerTitle]);
  
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
    console.log('audioFile 🍷', audioFile);
    initialRec(audioFile);
    // AudioRecord.stop();
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
    console.log('upload');
    console.log('🧑‍🚀🧑‍🚀', fileUrl);
    let formData = new FormData();
    formData.append('audioFile', {
      uri: 'file:///data/user/0/com.easy_boiler/files/test.wav',
      type: 'audio/wav',
      name: 'test.wav',
    });
    formData.append('flag', 'name');
    console.log(formData);

    fetch(`${BASE_URL}/language`, {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((response) => {
        console.log('response 🔥', response.flag);
        console.log(response);
        if (response.flag != 'navigation-error') {
          navigation.navigate(response.flag);
        } else {
          console.log('route error');
        }
      })
      .catch((err) => console.error(err));
  };

  const chooseEnglish = () => {
    AsyncStorage.setItem('language','en')
    setAppLanguage(en)
    AsyncStorage.setItem('appLanguage', en)
    navigation.navigate('language-success')
  }

  const chooseTamil = () => {
    AsyncStorage.setItem('language','ta')
    setAppLanguage(ta)
    AsyncStorage.setItem('appLanguage', ta)
    navigation.navigate('language-success')
  }

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
        }}>
        <View style={{padding: 20, margin: 10, backgroundColor: 'white'}}>
          <Text style={{textAlign: 'center', fontSize: 18}}>Welcome</Text>
          <Text style={{textAlign: 'center', fontFamily: Fonts.type.italic}}>
            {/* {username + ' ' + password} */}
            Test User
          </Text>
        </View>
        
        <Text style={{fontSize: 20, textAlign: 'center', padding: 20}} accessible={true} accessibilityLabel={`Choose a Language to Continue`} accessibilityRole="text">
          Choose a language to Continue
        </Text>
        <ButtonX
          accessible={true}
          accessibilityLabel="English"
          accessibilityHint="Click to Select English as your Language."
          accessibilityRole="button"
          dark={true}
          color={theme.colors.primary}
          onPress = {() => Tts.speak('Long Press to Select English')}
          onLongPress={() => chooseEnglish()}
          label={translations['englishLabel']}
        />
        <ButtonX
          accessible={true}
          accessibilityLabel="Profile"
          accessibilityHint="Click to Select Tamil as your Language."
          accessibilityRole="button"
          dark={true}
          color={theme.colors.primary}
          onPress={() => Tts.speak('தமிழைத் தேர்ந்தெடுக்க நீண்ட நேரம் அழுத்தவும்')}
          onLongPress={() => chooseTamil()}
          label={translations['tamilLabel']}
        />
        
        <View style={{alignItems: 'center', width: '100%'}}>
          <TouchableOpacity onPress={record}>
            <View
              style={{
                alignItems: 'center',
                padding: 10,
                marginTop: 10,
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
