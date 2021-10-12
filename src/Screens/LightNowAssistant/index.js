/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useContext} from 'react';
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
// import { Voice } from 'react-native-voice';
import AsyncStorage from '@react-native-community/async-storage';
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

    const options = {
      sampleRate: 16000, // default 44100
      channels: 1, // 1 or 2, default 1
      bitsPerSample: 16, // 8 or 16, default 16
      audioSource: 6, // android only (see below)
      wavFile: 'test.wav', // default 'audio.wav'
    };

    AudioRecord.init(options);
    Tts.speak(
      translations['voiceAssistantTts'],
      {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      },
    );

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
      if (menuitem.includes("coupon") || menuitem.includes("கூப்பன்")) {
        // Get offers from the API
        var url = 'get_coupons'

        fetch(`${BASE_URL}${url}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
          .then((response) => response.json())
          .then((response) => {
            console.log(response.data)
            if (response.data.length > 0) {
              storeDataCoupons(response.data)
              // Get offers from the API
              navigation.navigate('allOffers')
            }
          })
          .catch((err) => console.error(err));

        navigation.navigate('allCoupons')
      } else if (menuitem.includes("offers") || menuitem.includes("சலுகை")) {
        if (language == 'en') {
          var url = 'get_offers?id=1&lang=en'

          // Get offers from the API
          fetch(`${BASE_URL}${url}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
            .then((response) => response.json())
            .then((response) => {
              console.log(response.data)
              if (response.data.length > 0) {
                storeDataOffers(response.data)
                // Get offers from the API
                navigation.navigate('allOffers')
              }
            })
            .catch((err) => console.error(err));

          navigation.navigate('allOffers')
        } else {
          var url = 'get_offers?id=1&lang=ta'

          
          // Get offers from the API
          fetch(`${BASE_URL}${url}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
            .then((response) => response.json())
            .then((response) => {
              console.log(response.data)
              if (response.data.length > 0) {
                storeDataOffers(response.data)
                // Get offers from the API
                navigation.navigate('allOffers')
              }
            })
            .catch((err) => console.error(err));
        }
      } else if (menuitem.includes("profile") || menuitem.includes("சுயவிவரம்")) {
        navigation.navigate('profile')
      } else if (menuitem.includes("order") || menuitem.includes("ஒர்டெர்")) {
        // Get All Orders

        var url = null;
        if (language == 'en') {
          var url = `order/details?userId=${userId}&lang=en`
        } else {
          var url = `order/details?userId=${userId}&lang=ta`
        }
        
        // Get offers from the API
        fetch(`${BASE_URL}${url}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
          .then((response) => response.json())
          .then((response) => {
            console.log(response.data)
            if (response.data.length > 0) {
              storeDataOrders(response.data)
              // Get offers from the API
              navigation.navigate('orderMenu')
            }
          })
          .catch((err) => console.error(err));
      } else if (menuitem.includes("go back") || menuitem.includes("திரும்பி செல்")) {
        navigation.navigate('language-success');
      }

      setIsRecording(false)
    }
  }

  const storeDataOrders = async (value) => {
    try {
      await AsyncStorage.setItem('@allorders', value);
      console.log(value);
    } catch (e) {}
  }

  const storeDataCoupons = async (value) => {
    try {
      await AsyncStorage.setItem('@allcoupons', value);
      console.log(value);
    } catch (e) {}
  }

  const storeDataOffers = async (value) => {
    try {
      // const jsonValue = JSON.stringify(value);
      await AsyncStorage.setItem('@alloffers', value);
      console.log(value);
    } catch (e) {}
  };

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
    formData.append('orderId', 3);
    console.log(formData);

    fetch(`${BASE_URL}/voicebot/en`, {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: formData,
    })
      .then((response) => response.json())
      // .then((response) => response.json())
      .then((response) => {
        console.log('response ', response.flag);
        console.log(response);
        if (response.flag == 'back') {
          navigation.navigate('language-success');
        }
        if (response.flag == 'command-error') {
          Tts.speak(response.msg, {
            androidParams: {
              KEY_PARAM_PAN: -1,
              KEY_PARAM_VOLUME: 0.5,
              KEY_PARAM_STREAM: 'STREAM_MUSIC',
            },
          });
        }
        if (response.flag == 'list-coupon-success') {
          navigation.navigate('list-coupon-success');
        }
        if (response.flag == 'list-offer-success') {
          const resDataNews = response;
          storeData(response);
          console.log(resDataNews.listOffers);

          // navigation.navigate('list-offer-success', resDataNews);
        }
        if (response.flag == 'coupon-success') {
          navigation.navigate('coupon-success');
        }
        if (response.flag == 'offer-success') {
          navigation.navigate('offer-success');
        }
        if (response.flag == 'order-menu') {
          navigation.navigate('order-menu');
        }
        if (response.flag == 'order-completed') {
          navigation.navigate('order-completed', {
            response,
          });
        }
        if (response.flag == 'order-cancelled') {
          navigation.navigate('order-cancelled', {
            response,
          });
        }
        if (response.flag == 'navigation-error') {
          Tts.speak(response.msg, {
            androidParams: {
              KEY_PARAM_PAN: -1,
              KEY_PARAM_VOLUME: 0.5,
              KEY_PARAM_STREAM: 'STREAM_MUSIC',
            },
          });
        }
        // if (!response.flag == 'navigation-error') {
        //   navigation.navigate(response.flag);
        // } else {
        //   console.log('route error');
        // }

        // console.log(JSON.stringify(response));
      })
      .catch((err) => console.error(err));
  };
  const storeData = async (value) => {
    try {
      const jsonValue = JSON.stringify(value);
      await AsyncStorage.setItem('@offer_search', jsonValue);
      console.log(jsonValue);
      navigation.navigate('allOffers');
    } catch (e) {}
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
          <Text
            style={{fontSize: 20, textAlign: 'center', padding: 10}}
            accessible={true}
            accessibilityLabel={translations['voiceAssistantWelcomeText']}
            accessibilityRole="text"
          >
            {translations['voiceAssistantWelcomeText']}
          </Text>
          <ButtonX
            accessible={true}
            accessibilityLabel={translations['voiceAssistantCoupons']}
            accessibilityHint={translations['voiceAssistantCouponsHint']}
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress={() => navigation.navigate('allCoupons')}
            label={translations['voiceAssistantCoupons']}
          />
          <ButtonX
            accessible={true}
            accessibilityLabel={translations['voiceAssistantOffersNearMe']}
            accessibilityHint={translations['voiceAssistantOffersNearMeHint']}
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress={() => navigation.navigate('allOffers')}
            label={translations['voiceAssistantOffersNearMe']}
          />
          <ButtonX
            accessible={true}
            accessibilityLabel={translations['voiceAssistantOrder']}
            accessibilityHint={translations['voiceAssistantOrderHint']}
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress={() => navigation.navigate('orderMenu')}
            label={translations['voiceAssistantOrder']}
          />
          <ButtonX
            accessible={true}
            accessibilityLabel={translations['voiceAssistantProfile']}
            accessibilityHint={translations['voiceAssistantProfileHint']}
            accessibilityRole="button"
            dark={true}
            color={theme.colors.primary}
            onPress={() => navigation.navigate('profile')}
            label={'My Profile'}
          />
          <View style={{alignItems: 'center'}}>
            <TouchableOpacity 
              onPress={record}
              accessible={true}
              accessibilityLabel={translations['micLabel']}
              accessibilityHint={translations['micMenuLabel']}
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
