/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useContext, useState} from 'react';
import {View, Text, ScrollView} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {Container, HeaderButton} from '../../Components';
import useAppTheme from '../../Themes/Context';
import {IconX, ICON_TYPE} from '../../Icons';
import {useStoreState} from 'easy-peasy';
import Fonts from '../../Themes/Fonts';
import {TouchableOpacity} from 'react-native';
import {ButtonX} from '../../Components';
import metrics from '../../Themes/Metrics';
import AudioRecord from 'react-native-audio-record';
import AsyncStorage from '@react-native-community/async-storage';
import Tts from 'react-native-tts';
import { Avatar, Button, Card, Title, Paragraph } from 'react-native-paper';
import { LocalizationContext } from '../../Translations';
import { Voice } from '@react-native-voice/voice';

const MainScreen = ({routes, route, navigation}) => {
  const [resList, setListData] = useState('');
  const [offersList, setOffersList] = useState([]);

  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"

  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));

  const {
    translations,
  } = useContext(LocalizationContext);

  useEffect(() => {
    // Load Data from Async Storage
    Tts.speak(translations['allOffersTts'])

    getData()

    Voice.onSpeechStart = onSpeechStart()
    Voice.onSpeechRecognized = onSpeechRecognized()
    Voice.onSpeechResults = onSpeechResults()

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
      if (menuitem.includes("go back") || menuitem.includes("திரும்பி செல்")) {
        navigation.navigate('language-success');
      }
      setIsRecording(false)
    }
  }

  const createData = () => {
    var offers = []
    for (var i = 0; i < 5; i++) {
      offers.push({"item_id":i,"item_name":"Rice","item_price":i*10,"item_offer_price":i*10-(2*1),"shop_id":1,"shop_name":"Taniya"})
    }

    for (var i = 6; i < 11; i++) {
      offers.push({"item_id":i,"item_name":"Rice","item_price":i*10,"item_offer_price":i*10-(2*1),"shop_id":2,"shop_name":"Wijesuriya Stores"})
    }

    setOffersList(offers);
  };

  const getData = async () => {
    try {
      const offers = await AsyncStorage.getItem('@alloffers');

      var allOffers=[]
      var count=0;

      for (var i=0; i < offers.length; i++) {
        for (var j=0; j < offers[i].item.length; j++) {
          allOffers.push({"item_id": count, "shop_name": offers[i].shop.shopObj.shop_name, "shop_address": offers[i].shop.shopObj.shop_address, "item_name": offers[i].item[j].name, "item_price": offers[i].item[j].price, "item_offer_price": offers[i].item[j].item_offer_price})
        }
      }

      setOffersList(allOffers)

      // Read offers to the user
      for (var i=0; i < allOffers.length; i++) {
        Tts.speak(translations.formatString(translations['offerReadTts'], {shop_name: allOffers[i].shop_name, shop_address: allOffers[i].shop_address, item_name: allOffers[i].item_name, item_price: allOffers[i].item_price, item_offer_price: allOffers[i].item_offer_price},
        {
          androidParams: {
            KEY_PARAM_PAN: -1,
            KEY_PARAM_VOLUME: 0.5,
            KEY_PARAM_STREAM: 'STREAM_MUSIC',
          }
        }));
      }
    } catch (e) {
      console.log('ee');
      // error reading value
    }
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
    console.log('audioFile 🍷🍷', audioFile);
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
    console.log('upload 🧑‍🚀', fileUrl);
    let formData = new FormData();
    formData.append('audioFile', {
      uri: 'file:///data/user/0/com.easy_boiler/files/test.wav',
      type: 'audio/wav',
      name: 'test.wav',
    });
    formData.append('flag', 'name');
    console.log(formData);

    fetch('http://b0a48274d10c.ngrok.io/navigation/en', {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      body: formData,
    })
      .then((response) => response.json())
      // .then((response) => response.json())
      .then((response) => {
        console.log('response 🔥', response.flag);
        console.log(response);
        if (!response.flag != 'navigation-error') {
          navigation.navigate(response.flag);
        } else {
          console.log('route error');
        }

        // console.log(JSON.stringify(response));
      })
      .catch((err) => console.error(err));
  };

  return (
    <LoadingActionContainer fixed>
      <Container
        style={{
          padding: 10,
        }}>
        <ScrollView>
          <View
            style={{
              flex: 1,
              flexDirection: 'column',
              justifyContent: 'space-around',
            }}>
            <View
              style={{
                width: metrics.screenWidth * 0.95,
                height: '100%',
                borderRadius: 10,
              }}>
              {
                offersList.map(offer => {

                  return(
                  <Card
                  style={{display: 'flex', justifyContent: 'space-between', flexDirection: 'row', width: '100%', marginTop: 10}}
                  accessible={true}
                  accessibleRole=""
                  accessibilityLabel={translations.formatString(translations['offerLabel'], {item_name: offer.item_name})}
                  accessibilityHint={translations.formatString(translations['offerLabel'], {item_name: offer.item_name})}
                  key={offer.item_id}
                  >
                    <Card.Content>
                    <View style={{flex: 1, flexDirection: 'row'}}>
                        <View style={{
                            flexGrow: 1,
                        }}>
                        <Title style={{textAlign: 'center'}}>{offer.item_name}</Title>
                        <Paragraph style={{textAlign: 'center'}}>
                          {offer.shop_name}
                        </Paragraph>
                        </View>
                        <View style={{
                          width: 100,
                        }}>      
                          <Paragraph style={{textAlign: 'center'}}>
                            <Text style={{fontSize: 14}} accessible={true} accessibilityRole="text" accessibilityLabel={translations.formatString(translations['offerPriceLabel'], {item_name: offer.item_name, item_price: offer.item_price})}>
                              {translations['currencyLabel']} {offer.item_offer_price}
                            </Text>{"\n"}
                            <Text style={{fontSize: 12, textDecorationLine: 'line-through', textDecorationStyle: 'solid'}} accessible={true} accessibilityRole="text" accessibilityLabel={translations.formatString(translations['originalPriceLabel'], {item_name: offer.item_name, item_offer_price: offer.item_offer_price})}>
                            {translations['currencyLabel']} {offer.item_offer_price}
                            </Text>{"\n"}
                          </Paragraph>
                        </View>
                      </View>
                    </Card.Content>
                  </Card>
                  )
                })
              }
            </View>
          </View>
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
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
