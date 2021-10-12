/* eslint-disable react-native/no-inline-styles */
import React, {useRef, useContext, useState, useEffect} from 'react';
import {Text, Keyboard, Platform, PermissionsAndroid, TextInput} from 'react-native';
import {useStoreState, useStoreActions} from 'easy-peasy';
import {STATUS} from '../../Constants';
import {View} from 'react-native';
import {TouchableOpacity} from 'react-native';
import {IconX, ICON_TYPE} from '../../Icons';
import AudioRecord from 'react-native-audio-record';
import {BASE_URL} from '../../Config/index';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
// import Voice from '@react-native-voice/voice';
var RNFS = require('react-native-fs');
import {
  Section,
  Container,
  PasswordInputX,
  InputX,
  ButtonX,
} from '../../Components';
import {Buffer} from 'buffer';
import useAppTheme from '../../Themes/Context';
import useAuth from '../../Services/Auth';
import {showInfoToast} from '../../Lib/Toast';
import BottomPanel from '../../Components/Panel';
import Fonts from '../../Themes/Fonts';
import RNFetchBlob from 'rn-fetch-blob';
import Tts from 'react-native-tts';
// import { Voice } from 'react-native-voice';

export default ({navigation}) => {
  const [locale, setLocale] = useState('en_us');
  const [isRecording, setIsRecording] = useState(false);

  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"

  useEffect(() => {
    console.log('running');

    Voice.onSpeechStart = onSpeechStart()
    Voice.onSpeechRecognized = onSpeechRecognized()
    Voice.onSpeechResults = onSpeechResults()

    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };
    requestCameraPermission();
    requestAudioPermission();
    requestLocationPermission();
    AudioRecord.init(options);

    const interval = setInterval(() => {
      if (!isRecording) {
        // Not Recording username or password
        Voice.stop() // Stop Recording
        Voice.start(locale) // Start Recording Again
      }
    }, 5000);
  
    return () => clearInterval(interval); // This represents the unmount function, in which you need to clear your interval to prevent memory leaks.
  }, []);

  const {
    translations,
    appLanguage,
    setAppLanguage,
    initializeAppLanguage,
  } = useContext(LocalizationContext); // 1
  initializeAppLanguage(); // 2

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
      setIsRecording(false)
    }
  }

  const requestCameraPermission = async () => {
    console.log('hell 👋');
    try {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.RECORD_AUDIO,
        {
          title: 'LightNowApp Camera Permission',
          message:
            'LightNowApp needs access to your camera ' +
            'so you can take pictures of lists.',
          buttonNeutral: 'Ask Me Later',
          buttonNegative: 'Cancel',
          buttonPositive: 'OK',
        },
      );
      if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        console.log('You can use the camera');
      } else {
        console.log('Camera permission denied');
      }
    } catch (err) {
      console.warn(err);
    }
  };
  const requestLocationPermission = async () => {
    try {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
        {
          title: 'LightNowApp Location Permission',
          message:
            'LightNowApp needs to access your device\'s location ' +
            'so you can place orders at your nearest shops.',
            buttonNeutral: 'Ask Me Later',
            buttonNegative: 'Cancel',
            buttonPositive: 'OK',
        },
      );
      if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        console.log('Your location can now be accessed.');
      } else {
        console.log('Location Access cannot be accessed yet.');
      }
    } catch (err) {
      console.warn(err);
    }
  }

  const requestAudioPermission = async () => {
    try {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.CAMERA,
        {
          title: 'LightNowApp AudioRecord Permission',
          message: 'LightNowApp access to your microphone ',
          buttonNeutral: 'Ask Me Later',
          buttonNegative: 'Cancel',
          buttonPositive: 'OK',
        },
      );
      if (granted === PermissionsAndroid.RESULTS.GRANTED) {
        console.log('You can use the audioRecord');

        // Start Listening to the User
        Voice.start(locale);
      } else {
        console.log('audioRecord permission denied');
      }
    } catch (err) {
      console.warn(err);
    }
  };

  const onChange = useStoreActions(
    (actions) => actions.login.onLoginInputChange,
  );
  const {t} = useTranslation();
  const {login} = useAuth();
  const {theme} = useAppTheme();

  const inputUserName = useRef();
  const inputPassword = useRef();

  const panelRef = useRef();

  const onSubmit = () => {
    inputPassword.current.focus();
  };

  const {username, password, status} = useStoreState((state) => ({
    username: 'TestUser',
    password: 'state.login.password',
    status: state.login.status,
  }));

  const loginUser = () => {
    Keyboard.dismiss();

    if (!username || !password) {
      showInfoToast('Username and password are mandatory, try again !');
    }

    login({
      username,
      password,
    });
  };

  const record = () => {
    console.log('record');

    AudioRecord.start();
  };
  const initialRec = (audioFile) => {
    uploadVideo(audioFile);
    // postData2(audioFile);
    console.log('initialRec', audioFile);
    let dirs = RNFetchBlob.fs.dirs;
    // console.log('dir 🛀🛀🛀', dirs);
    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };
  };

  const stopRecord = async () => {
    console.log('recordStop ');
    const audioFile = await AudioRecord.stop();
    AudioRecord.on('data', (data) => {
      // const chunk = Buffer.from(data, 'base64');
      // console.log('chunk', chunk);
    });
    console.log('audioFile latees 🍷🍷', audioFile);
    initialRec(audioFile);
    // AudioRecord.stop();
  };

  const uploadVideo = async (fileUrl) => {
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

    fetch(`${BASE_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: formData,
    })
      .then((response) => response.json())
      // .then((response) => response.json())
      .then((response) => {
        console.log('response 🤡🤡');
        console.log(response);
        login({
          username,
          password,
        });
        // console.log(JSON.stringify(response));
      })
      .catch((err) => console.error(err));
  };

  const loading = status === STATUS.FETCHING;

  return (
    <Container>
      <LoadingActionContainer>
        <Section>
          <Text
            style={{
              textAlign: 'center',
              fontSize: 30,
              color: theme.colors.primary,
              marginTop: 60,
              fontFamily: 'Roboto',
              marginBottom: 20,
              accessible: true,
              accessibilityLabel: "LightNow"
            }}>
            {`LightNow`}
          </Text>
        </Section>
        <Section>
          <Text
            style={{
              fontSize: 20,
              textAlign: 'center',
              fontFamily: 'Roboto',
              color: theme.colors.primaryText,
              accessible: true,
              accessibilityLabel: translations['loginLabel']
            }}>
              {translations['loginLabel']} 
          </Text>
        </Section>
        <Section>
          <InputX
            accessible={true}
            label={translations['usernameLabel']}
            accessibilityLabel={translations['usernameLabel']}
            // mode="outlined"
            ref={inputUserName}
            style={{backgroundColor: '#fafafa'}}
            autoCapitalize="none"
            returnKeyType={'next'}
            onSubmitEditing={onSubmit}
            onChangeText={(text) =>
              onChange({
                key: 'username',
                value: text,
              })
            }
            value={username}
          />
          <PasswordInputX
            accessible={true}
            label={translations['passwordLabel']}
            accessibilityLabel={translations['passwordLabel']}
            ref={inputPassword}
            value={password}
            // mode="outlined"
            style={{backgroundColor: '#fafafa'}}
            returnKeyType={'go'}
            onSubmitEditing={loginUser}
            onChangeText={(text) =>
              onChange({
                key: 'password',
                value: text,
              })
            }
          />
        </Section>
        <Section>
          <View style={{alignItems: 'center'}}>
            {/* <TouchableOpacity onPress={uploadVideo}> */}
            <TouchableOpacity onLongPress={record} accessible={true} accessibilityLabel={translations['loginLongPress']}>
              <View
                style={{
                  padding: 10,
                  marginTop: 10,
                  backgroundColor: theme.colors.secondary,
                  borderRadius: 10,
                }}>
                <IconX name={'md-mic'} style={{color: '#ff3f'}} />
              </View>
            </TouchableOpacity>
            <TouchableOpacity onLongPress={stopRecord} accessible={true} accessibilityLabel={translations['loginLongPress']}>
              <View
                style={{
                  padding: 10,
                  marginTop: 10,
                  backgroundColor: theme.colors.primary,
                  borderRadius: 10,
                }}>
                <IconX name={'md-mic'} style={{color: '#fff'}} />
              </View>
            </TouchableOpacity>
          </View>
          <ButtonX
            label={translations['loginButton']}
            accessible={true}
            accessibilityLabel={translations['loginButton']}
            accessibilityRole="button"
            loading={loading}
            dark={true}
            color={loading ? theme.colors.accent : theme.colors.primary}
            onPress={loginUser}
            label={t('Login')}
          />
        </Section>
      </LoadingActionContainer>

      <BottomPanel ref={panelRef} />
    </Container>
  );
};
