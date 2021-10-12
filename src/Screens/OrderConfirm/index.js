/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useContext, useState} from 'react';
import {View, Text, ScrollView} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {Container, HeaderButton, InputX} from '../../Components';
import useAppTheme from '../../Themes/Context';
import {IconX, ICON_TYPE} from '../../Icons';
import {useStoreState} from 'easy-peasy';
import Fonts from '../../Themes/Fonts';
import {TouchableOpacity, ListItem} from 'react-native';
import AudioRecord from 'react-native-audio-record';
import {BASE_URL} from '../../Config/index';
import Tts from 'react-native-tts';
import {ButtonX} from '../../Components';
import { Avatar, Button, Card, Title, Paragraph } from 'react-native-paper';
import AsyncStorage from '@react-native-community/async-storage';
import {LocalizationContext} from '../../Translations';
import { Voice } from '@react-native-voice/voice';

const MainScreen = ({routes, route, navigation}) => {
  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));
  const [resData, setResData] = useState('');
  const [theArray, setTheArray] = useState(route.params);
  const [language, setLanguage] = useState('en');
  const [languageTts, setLanguageTts] = useState('en-IN');
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

    // Load the Chosen Language
    setLanguage(AsyncStorage.getItem('language'))

    if (language == 'ta') {
      setLanguageTts('ta-IN')
    } else {
      setLanguageTts('en-IN')
    }

    Tts.setDefaultLanguage(languageTts)
    Tts.speak(
      translations.formatString(translations['orderConfirmTts'], {total: totalAmount}),
      {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      },
    );

    var totalAmount=0
    for (var i=0; i < theArray.items.length; i++) {
      if (theArray.items[i].item_offer_price == null || theArray.items[i].item_offer_price <= 0) {
        Tts.speak(translations.formatString(translations['readListConfirmTts'], {item_name: theArray.items[i].item_name, item_qty: theArray.items[i].item_qty, item_price: theArray.items[i].item_price}))
        totalAmount += (theArray.items[i].item_price * theArray.items[i].item_qty)
      } else {
        Tts.speak(translations.formatString(translations['readListConfirmTts'], {item_name: theArray.items[i].item_name, item_qty: theArray.items[i].item_qty, item_price: theArray.items[i].item_offer_price}))
        totalAmount += theArray.items[i].item_offer_price * theArray.items[i].item_qty
      }
    }

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
      if (menuitem.includes("read") || menuitem.includes("படி")) {
        // Read the Results
        read()
      } else if (menuitem.includes("continue") || menuitem.includes("தொடரும்")) {
        // Call Api to Checkout and Complete Process
        // var couponId = await AsyncStorage.getItem('couponId')
        let formdata = FormData()
        formdata.append(theArray)

        fetch(`${BASE_URL}/voicesearch/en`, {
          method: 'POST',
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          body: formData,
        })
          .then((response) => response.json())
          .then((response) => {
            console.log(response)
            // Successfully Completed Order.
            navigation.navigate('orderSuccess')
          })
          .catch((err) => console.error(err));

        navigation.navigate('orderSuccess')
      } else if (menuitem.includes("go back") || menuitem.includes("திரும்பி செல்")) {
        navigation.navigate('language-success');
      }

      setIsRecording(false)
    }
  }

  useEffect(() => {
    if (language == 'ta') {
      setLanguageTts('ta-IN')
    } else {
      setLanguageTts('en-IN')
    }

    AsyncStorage.setItem('language', language);
  }, [language]);

  const record = () => {
    console.log('record');

    setTheArray(cartitems)

    AudioRecord.start();
    timeout;
    let timeout = setTimeout(() => {
      stopRecord();
      console.log('hello');
    }, 12000);
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
    formData.append('userId', 3);

    fetch(`${BASE_URL}/voicesearch/en`, {
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

        if (response.flag == 'back') {
          navigation.navigate('language-success');
        }
        if (response.flag == 'place-order') {
          navigation.navigate('place-order', {
            response,
          });
        }
        if (response.flag == 'search-save') {
          navigation.navigate('search-save', {
            response,
          });
        }
        if (response.flag == 'check-order') {
          navigation.navigate('check-order');
        }
        if (response.flag == 'checkout') {
          Tts.speak(response.msg, {
            androidParams: {
              KEY_PARAM_PAN: -1,
              KEY_PARAM_VOLUME: 0.5,
              KEY_PARAM_STREAM: 'STREAM_MUSIC',
            },
          });
          navigation.navigate('language-success');
        }
        if (response.flag == 'search-success') {
          setResData(response);
          setTheArray([...theArray, response.item]);
          Tts.speak(response.msg, {
            androidParams: {
              KEY_PARAM_PAN: -1,
              KEY_PARAM_VOLUME: 0.5,
              KEY_PARAM_STREAM: 'STREAM_MUSIC',
            },
          });
        } else {
          Tts.speak(response.msg, {
            androidParams: {
              KEY_PARAM_PAN: -1,
              KEY_PARAM_VOLUME: 0.5,
              KEY_PARAM_STREAM: 'STREAM_MUSIC',
            },
          });
        }
      })
      .catch((err) => console.error(err));
  };

  const read = () => {
    // await AsyncStorage.getItem('userAddress')
    Tts.speak(translations.formatString(translations['addressTextTts'], {address: ""}))
    Tts.speak(translations.formatString(translations['orderConfirmTts'], {total: totalAmount}))
    Tts.speak(translations['cashOnDeliveryLabel'])
  }

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
          flex: 1
        }}>
        

        <ScrollView>
          <Card style={{marginTop: 10}}>
              <Card.Content>
                <Text>{translations['addressLabel']}: <Text style={{textAlign: 'right'}}>{`Address`}</Text></Text>
              </Card.Content>
            </Card>

            <Card style={{marginTop: 10}}>
              <Card.Content>
                <Text>{translations['totalAmountLabel']}: <Text style={{textAlign: 'right'}}>{totalAmount}</Text></Text>
              </Card.Content>
            </Card>

            <Card style={{marginTop: 10}}>
              <Card.Content>
                <Text>{translations['paymentMethodLabel']}: <Text style={{textAlign: 'right'}}>{translations['cashOnDeliveryLabel']}</Text></Text>
              </Card.Content>
            </Card>
        </ScrollView>

        <View style={{alignItems: 'center'}}>
          <TouchableOpacity
            style={{width: '100%'}}
            onPress={record}
            accessible={true}
            accessibilityLabel={translations['micLabel']}
            accessibilityHint={translations['micMenuLabel']}
            accessibilityRole="button"
          >
            <View
              style={{
                alignItems: 'center',
                padding: 10,
                marginTop: 20,
                backgroundColor: theme.colors.primary,
                borderRadius: 10,
              }}>
              <IconX name={'md-mic'} style={{color: '#fff'}} />
            </View>
          </TouchableOpacity>
        </View>

        <View style={{alignItems: 'center'}}>
          <ButtonX
            style={{width: '100%'}}
            dark={true}
            color={theme.colors.primary}
            label={translations['confirmOrder']}
            onPress={() => navigation.navigate('orderSuccess')}
            accessibile={true}
            accessibilityLabel={translations['btnConfirmOrderLongPress']}
            accessibilityRole="button"
          />
        </View>
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
