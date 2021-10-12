/* eslint-disable react-native/no-inline-styles */
import React, { useEffect, useContext, useState } from 'react';
import { View, Text, ScrollView, Alert } from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import { Container, HeaderButton, InputX } from '../../Components';
import useAppTheme from '../../Themes/Context';
import { IconX, ICON_TYPE } from '../../Icons';
import { useStoreState } from 'easy-peasy';
import Fonts from '../../Themes/Fonts';
import { TouchableOpacity, ListItem } from 'react-native';
import AudioRecord from 'react-native-audio-record';
import { BASE_URL } from '../../Config/index';
import Tts from 'react-native-tts';
import { ButtonX } from '../../Components';
import { Avatar, Button, Card, Title, Paragraph } from 'react-native-paper';
import AsyncStorage from '@react-native-community/async-storage';
import { LocalizationContext } from '../../Translations';
import { Voice } from '@react-native-voice/voice';

const MainScreen = ({ routes, route, navigation }) => {
  const { theme } = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const { username, password } = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));
  const [resData, setResData] = useState('');
  const [language, setLanguage] = useState('en');
  const [languageTts, setLanguageTts] = useState('en-IN');
  const [allItems, setAllItems] = useState(route.params);
  const [pharmaceuticalItems, setPharmaceuticalItems] = useState(null);
  const [prescriptionItems, setPrescriptionItems] = useState(null);
  const [availableItems, setAvailableItems] = useState(null);
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

    // Iterate Items and Store Pharmaceutical and Prescription Items
    var pharmaceutical=[]
    var prescription=[]
    for (var i =0; i < allItems.items.length; i++) {
      if (allItems.items[i].availability == 1) {
        if (allItems.items[i].pharmaceutical == true) {
          pharmaceutical.push(allItems.items[i])
        }

        if (allItems.items[i].prescription == true) {
          prescription.push(allItems.items[i])
        }
      }
    }
    
    setPharmaceuticalItems(pharmaceutical)
    setPrescriptionItems(prescription)

    // Load the Chosen Language
    setLanguage(AsyncStorage.getItem('language'))

    if (language == 'ta') {
      setLanguageTts('ta-IN')
    } else {
      setLanguageTts('en-IN')
    }

    Tts.setDefaultLanguage(languageTts)
    Tts.speak(
      translations['voiceSearchPharmaTts'],
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

    // Read items
    read()
  
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
      } else if (menuitem.includes("continue") || menuitem.includes("தொடரும்")) {
        navigation.navigate('checkout')
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

    setAllItems(cartitems)

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
    AudioRecord.on('data', (data) => { });
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
          setAllItems([...theArray, response.item]);
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
    // Read Pharmaceutical Items and Prescription Items
    Tts.speak(translations['pharmaItemsText'])
    for (var i=0; i < pharmaceuticalItems.length; i++) {
      Tts.speak(translations.formatString(translations['readListTts'], {item_name: pharmaceuticalItems[i].item_name, item_qty: pharmaceuticalItems[i].item_name}))
    }

    Tts.speak(translations['pharmaPrescriptionText'])
    for (var i=0; i < prescriptionItems.length; i++) {
      Tts.speak(translations.formatString(translations['readListTts'], {item_name: prescriptionItems[i].item_name, item_qty: prescriptionItems[i].item_qty}))
    }
  }

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
          flex: 1
        }}>

          <Title style={{ marginTop: 10 }}>{translations['pharmaItemsText']}</Title>
          <ScrollView horizontal={true} style={{marginTop: 10}}>
            {pharmaceuticalItems && pharmaceuticalItems.length > 0 ? pharmaceuticalItems.map((item) => {
              
              return (
                <Card style={{margin: 10}} key={item._id}>
                  <Card.Content>
                    <Paragraph style={{textAlign: 'left'}}>
                      <Text style={{fontSize: 16, textTransform: 'capitalize', textDecorationStyle: 'solid'}} accessibile={true} accessibilityLabel={item.item_name} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty}  ${item.item_unit}`} accessibilityRole="text">
                        {item.item_name}{"\n"}
                      </Text>
                      <Text style={{fontSize: 12}}>
                        {item.item_qty}{item.item_unit}
                      </Text>
                    </Paragraph>
                    <Paragraph style={{textAlign: 'center'}}>
                      {item.item_offer_price != null ?
                      <>
                      <Text accessibile={true} accessibilityLabel={`${item.item_qty}`} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty} ${item.item_unit}`}>
                        {translations['currencyLabel']}.{item.item_offer_price}/{item.item_unit}{"\n"}
                      </Text>
                      <Text style={{fontSize: 10,textDecorationLine: 'line-through', textDecorationStyle: 'solid'}} accessible={true} accessibilityLabel={`Original Price of ${item.item_name} is ${translations['currencyLabel']}.${item.item_price} and the Offer Price is ${translations['currencyLabel']}.${item.item_offer_price}`}>
                        {translations['currencyLabel']}.{item.item_price}/{item.item_unit}
                      </Text>
                      </>
                      : 
                      <Text accessibile={true} accessibilityLabel={`${item.item_qty}`} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty} ${item.item_unit}`}>
                        {translations['currencyLabel']}.{item.item_price}/{item.item_unit}
                      </Text>
                      }
                    </Paragraph>
                  </Card.Content>
                </Card>
              )
            }
            ) :
              <Text style={{fontSize: 14, color: '#e74c3c'}} accessible={true} accessibilityLabel={translations['noPharmaText']} accessibilityRole="text">
                {translation['noPharmaText']}
              </Text>
            }
            
          </ScrollView>

          <Title style={{ marginTop: 10 }}>{translations['pharmaPrescriptionText']}</Title>
          <ScrollView horizontal={true} style={{marginTop: 10}} accessible={true}>
            {prescriptionItems ? null : <Text style={{marginTop: 5, fontSize: 12}} accessible={true} accessibilityLabel={translations['pharmaProceedText']} accessibilityRole="text">{translations['pharmaProceedText']}</Text>}
            {prescriptionItems && prescriptionItems.length > 0 ? prescriptionItems.map((item) => {
              return (
                <Card style={{margin: 10}} key={item._id}>
                  <Card.Content>
                    <Paragraph style={{textAlign: 'left'}}>
                      <Text style={{fontSize: 16, textTransform: 'capitalize', textDecorationStyle: 'solid'}} accessibile={true} accessibilityLabel={item.item_name} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty}  ${item.item_unit}`} accessibilityRole="text">
                        {item.item_name}{"\n"}
                      </Text>
                      <Text style={{fontSize: 12}}>
                        {item.item_qty}{item.item_unit}
                      </Text>
                    </Paragraph>
                    <Paragraph style={{textAlign: 'center'}}>
                      {item.item_offer_price != null ?
                      <>
                      <Text accessibile={true} accessibilityLabel={`${item.item_qty}`} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty} ${item.item_unit}`}>
                        {translations['currencyLabel']}.{item.item_offer_price}/{item.item_unit}{"\n"}
                      </Text>
                      <Text style={{fontSize: 10,textDecorationLine: 'line-through', textDecorationStyle: 'solid'}} accessible={true} accessibilityLabel={`Original Price of ${item.item_name} is ${translations['currencyLabel']}.${item.item_price} and the Offer Price is ${translations['currencyLabel']}.${item.item_offer_price}`}>
                        {translations['currencyLabel']}.{item.item_price}/{item.item_unit}
                      </Text>
                      </>
                      : 
                      <Text accessibile={true} accessibilityLabel={`${item.item_qty}`} accessibilityHint={`This is an item ${item.item_name} with quantity ${item.item_qty} ${item.item_unit}`}>
                        {translations['currencyLabel']}.{item.item_price}/{item.item_unit}
                      </Text>
                      }
                    </Paragraph>
                  </Card.Content>
                </Card>
              )
            }
            ) : 
              <Text style={{fontSize: 14, color: '#e74c3c'}} accessible={true} accessibilityLabel={translations['noPrescText']} accessibilityRole="text">
                {translation['noPrescText']}
              </Text>
            }

          </ScrollView>

          <View style={{ alignItems: 'center' }}>
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
                <IconX name={'md-mic'} style={{ color: '#fff' }} />
              </View>
            </TouchableOpacity>
          </View>

          <View style={{alignItems: 'center'}}>
            <ButtonX
              style={{width: '100%'}}
              dark={true}
              color={theme.colors.primary}
              label={translations['btnPlacrOrder']}
              onPress = {() => Tts.speak(translations['btnPlaceOrderLongPress'])}
              onLongPress={() => navigation.navigate('checkout', allItems)}
              accessibile={true}
              accessibilityLabel="Continue to Place Order"
              accessibilityHint="Continue to Place Order"
              accessibilityRole="button"
            />
          </View>

          <View style={{alignItems: 'center'}}>
            <ButtonX
              style={{width: '100%'}}
              dark={true}
              color={theme.colors.primary}
              label={translations['btnAlter']}
              onPress = {() => Tts.speak(translations['btnAlterLongPress'])}
              onLongPress={() => navigation.navigate('voice-search', allItems)}
              accessibile={true}
              accessibilityLabel="Alter your Order"
              accessibilityHint="Alter your Order"
              accessibilityRole="button"
            />
          </View>
        
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
