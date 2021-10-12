/* eslint-disable react-native/no-inline-styles */
import React, {useState, useContext, useEffect} from 'react';
import {View, Text} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {Container, HeaderButton} from '../../Components';
import useAppTheme from '../../Themes/Context';
import {IconX, ICON_TYPE} from '../../Icons';
import {useStoreState} from 'easy-peasy';
import Fonts from '../../Themes/Fonts';
import {TouchableOpacity} from 'react-native';
import {ButtonX} from '../../Components';
import AudioRecord from 'react-native-audio-record';
import {BASE_URL} from '../../Config/index';
import Tts from 'react-native-tts';
import { LocalizationContext } from '../../Translations';
import { Voice } from '@react-native-voice/voice';

const MainScreen = ({routes, navigation}) => {
  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));

  const [language, setLanguage] = useState('en');
  const [languageTts, setLanguageTts] = useState('en-IN');
  const [locale, setLocale] = useState('en_us');
  const [isRecording, setIsRecording] = useState(false);

  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"
  
  const {
    translations,
  } = useContext(LocalizationContext);

  useEffect(() => {
    const _toggleDrawer = () => {
      navigation.toggleDrawer();
    };
    Voice.onSpeechStart = onSpeechStart()
    Voice.onSpeechRecognized = onSpeechRecognized()
    Voice.onSpeechResults = onSpeechResults()

    Tts.speak(translations['allOrdersTts'],
      {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      },
    );
    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };

    AudioRecord.init(options);

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
      if (menuitem.includes("pending") || menuitem.includes("நிலுவையில் உள்ளது")) {
        navigation.navigate('PendingOrdersList')
      } else if (menuitem.includes("complete") || menuitem.includes("முழுமை")) {
        navigation.navigate('completedOrdersList')
      } else if (menuitem.includes("cancel") || menuitem.includes("ரத்து")) {
        navigation.navigate('cancelledOrdersList')
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
    // formData.append('flag', 'name');
    console.log(formData);
    formData.append('userId', 3);
    fetch(`${BASE_URL}/voicebot/en`, {
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
        if (response.flag == 'order-completed') {
          navigation.navigate('order-completed', {
            response,
          });
        }
        if (response.flag == 'order-pending') {
          navigation.navigate('order-pending', {
            response,
          });
        }
        if (response.flag == 'order-cancelled') {
          navigation.navigate('order-cancelled', {
            response,
          });
        }
        // if (!response.flag != 'navigation-error') {
        //   navigation.navigate(response.flag);
        // } else {
        //   console.log('route error');
        // }
      })
      .catch((err) => console.error(err));
  };

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
        }}>
        <View
          style={{
            flex: 1,
            flexDirection: 'column',
            justifyContent: 'space-around',
          }}>
          <ButtonX
            accessible={true} 
            accessibilityLabel={translations['pendingOrdersLabel']}
            accessibilityHint={translations['pendingOrdersHint']}
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress = {() => Tts.speak(translations['pendingOrdersLongPress'])}
            onLongPress= {() => navigation.navigate('PendingOrdersList')}
            label={translations['pendingOrdersLabel']}
          />
          <ButtonX
            accessible={true} 
            accessibilityLabel={translations['completedOrdersLabel']} 
            accessibilityHint={translations['completedOrdersHint']}
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress = {() => Tts.speak(translations['completedOrdersLongPress'])}
            onLongPress= {() => navigation.navigate('completedOrdersList')}
            label={translations['completedOrdersLabel']}
          />
          <ButtonX
            accessible={true} 
            accessibilityLabel={translations['cancelledOrdersLabel']}
            accessibilityHint={translations['cancelledOrdersHint']}
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress = {() => Tts.speak(translations['cancelledOrdersLongPress'])}
            onLongPress= {() => navigation.navigate('cancelledOrdersList')}
            label={translations['cancelledOrdersLabel']}
          />

          <View style={{alignItems: 'center'}}>
            <TouchableOpacity
              onPress={record}
              accessible={true}
              accessibilityLabel={translations['micLabel']}
              accessibilityHint={translations['micMenyLabel']}
              accessibilityRole="button"
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
        </View>
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
