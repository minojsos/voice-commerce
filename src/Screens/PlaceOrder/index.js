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
import {ButtonX} from '../../Components';
import {BASE_URL} from '../../Config/index';
import AudioRecord from 'react-native-audio-record';
import { Avatar, Button, Card, Title, Paragraph } from 'react-native-paper';
import Tts from 'react-native-tts';
import AsyncStorage from '@react-native-community/async-storage';
import { LocalizationContext } from '../../Translations';
import { Voice } from '@react-native-voice/voice';
import { read } from 'react-native-fs';

const MainScreen = ({routes, route, navigation}) => {
  const {theme} = useAppTheme();
  // const {navigation} = this.props;
  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));

  const [allItems, setAllItems] = useState(route.params);
  const [shopDetails, setShopDetails] = useState([])
  const [availableItems, setAvailableItems] = useState([]);
  const [totalAmount, setTotalAmount] = useState(0)
  const [language, setLanguage] = useState('en');
  const [languageTts, setLanguageTts] = useState('en-IN');
  const [isRecording, setIsRecording] = useState(false);

  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"

  const {
    translations
  } = useContext(LocalizationContext)

  // const {otherParam} = route.params;
  useEffect(() => {
    Voice.onSpeechStart = onSpeechStart()
    Voice.onSpeechRecognized = onSpeechRecognized()
    Voice.onSpeechResults = onSpeechResults()

    // Load the Chosen Language
    setLanguage(AsyncStorage.getItem('language'))

    // Iterate All items and only store the Available items along with Shop Details
    var available=[]
    var total=0
    for (var i=0; i < allItems.items.length; i++) {
      if (allItems.items[i].availability == 1 && allItems.items[i].prescription == false) {
        available.push(allItems.items[i])
        if (allItems.items[i].item_offer_price != null && allItems.items[i].item_offer_price > 0) {
          total+=allItems.items[i].item_qty * allItems.items[i].item_offer_price;
        } else {
          total+=allItems.items[i].item_qty * allItems.items[i].item_price;
        }
      }
    }
    setTotalAmount(total)
    setAvailableItems(available)

    if (language == 'ta') {
      setLanguageTts('ta-IN')
    } else {
      setLanguageTts('en-IN')
    }

    Tts.setDefaultLanguage(languageTts)
    Tts.speak(
      translations['placeOrderTts'],
      {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      },
    );

    const _toggleDrawer = () => {
      navigation.toggleDrawer();
    };
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
        navigation.navigate('orderConfirm', {"shop_id":allItems.shop_id, "availability": allItems.perc, "shop_name": allItems.shopObj.shop_name, "shop_address": allItems.shopObj.shop_address, "shop_lat": allItems.shopObj.shop_lat, "shop_long": allItems.shopObj.shop_long, "items": availableItems})
      } else if (menuitem.includes("go back") || menuitem.includes("திரும்பி செல்")) {
        navigation.navigate('language-success');
      }

      setIsRecording(false)
    }
  }

  const names = ['Rice', 'Sugar', 'Flour'];

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
      })
      .catch((err) => console.error(err));
  };

  const read = () => {

  }

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
          flex: 1
        }}>
          
        <ScrollView style={{height: '75%'}}>
          <View
            style={{
              flex: 1,
              flexDirection: 'row',
            }}>
              <View
                style={{
                  flex: 1,
                  justifyContent: 'space-around',
                  paddingLeft: 20,
                  paddingTop: 20
                }}>
                <Text>{translations['nameLabel']}</Text>

                {names.map((name) => (
                  <Text>{name}</Text>
                ))}
              </View>
              <View
                style={{
                  flex: 1,
                  justifyContent: 'space-around',
                  paddingTop: 20
                }}>
                <Text>{translations['quantityLabel']}</Text>
                {names.map((name) => (
                  <Text>1</Text>
                ))}
              </View>
              <View
                style={{
                  flex: 1,
                  justifyContent: 'space-around',
                  paddingTop: 20
                }}>
                <Text>{translations['priceLabel']}</Text>
                {names.map((name) => (
                  <Text>Rs.100</Text>
                ))}
              </View>
              <View
                style={{
                  flex: 1,
                  justifyContent: 'space-around',
                  paddingTop: 20
                }}>
                <Text>Action</Text>
                {names.map((name) => (
                  <View style={{justifyContent: 'center', paddingTop: 20}}>
                    <TouchableOpacity>
                      
                      <IconX
                        style={{marginBottom: 5, alignItems: 'center', justifyContent: 'center'}}
                        origin={ICON_TYPE.FONT_AWESOME}
                        name={'times'}
                        color={theme.colors.primary}
                      />
                  
                    </TouchableOpacity>
                  </View>
                ))}
              </View>
          </View>
        </ScrollView>

        <View style={{width: '100%'}}>
          <Card style={{padding:10}}>
            <Card.Content>
              <Text style={{width: '100%'}}>{translations['totalAmountLabel']}: <Text style={{textAlign: 'right', fontWeight: '600'}}>{translations['currencyLabel']} {totalAmount}</Text></Text>
            </Card.Content>              
          </Card>
        </View>
        
        <View style={{alignItems: 'center', width: '100%'}}>
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

        <View style={{flexGrow: 1, alignItems: 'center'}}>
          <ButtonX
            style={{width: '100%'}}
            dark={true}
            color={theme.colors.primary}
            onPress = {() => Tts.speak(translations['btnConfirmOrderLongPress'])}
            onLongPress = {() => navigation.navigate('orderConfirm', {"shop_id":allItems.shop_id, "availability": allItems.perc, "shop_name": allItems.shopObj.shop_name, "shop_address": allItems.shopObj.shop_address, "shop_lat": allItems.shopObj.shop_lat, "shop_long": allItems.shopObj.shop_long, "items": availableItems})}
            label={translations['btnConfirmOrder']}
          />
        </View>
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
