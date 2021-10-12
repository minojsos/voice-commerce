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
  const [couponsList, setCouponsList] = useState([]);

  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));

  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"

  const {
    translations,
  } = useContext(LocalizationContext);

  useEffect(() => {
    getData()

    Voice.onSpeechStart = onSpeechStart()
    Voice.onSpeechRecognized = onSpeechRecognized()
    Voice.onSpeechResults = onSpeechResults()

    const _toggleDrawer = () => {
      navigation.toggleDrawer();
    };

    Tts.speak(translations['allCouponsTts']);

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
      } else if (menuitem.includes("coupon")) {
        var coupon_code = menuitem.split("coupon")
        if (coupon_code.length > 1 && coupon_code[1] != "") {
          for (var i=0; i < couponsList.length; i++) {
            if (couponsList[i].coupon_id == coupon_code[1] || couponsList[i].coupon_code == coupon_code[1]) {
              storeCoupon(couponsList[i])
              console.log("Coupon Code: "+coupon_code[1])
            }
          }
        }
      } else if (menuitem.includes("கூப்பன்")) {
        var coupon_code = menuitem.split("கூப்பன்")
        if (coupon_code.length > 1 && coupon_code[1] != "") {
          for (var i=0; i < couponsList.length; i++) {
            if (couponsList[i].coupon_id == coupon_code[1] || couponsList[i].coupon_code == coupon_code[1]) {
              storeCoupon(couponsList[i])
              console.log("Coupon Code: "+coupon_code[1])
            }
          }
        }
      }
      setIsRecording(false)
    }
  }

  const storeCoupon = async (value) => {
    var existing = await AsyncStorage.getItem('@selectedcoupon')
    if (existing == null) {
      // Make sure Seleccted Coupon is not existing already
      Tts.speak(translations.formatString(translations['couponAddedTts'], {coupon_code: value.coupon_id}))
      await AsyncStorage.setItem('@selectedcoupon', value)
    } else {
      Tts.speak(translations.formatString(translations['couponReplacedTts'], {coupon_code1: existing.coupon_id, coupon_code2: value.coupon_id}))
    }
  }

  const getData = async () => {
    try {
      const coupons = await AsyncStorage.getItem('@allcoupons');

      var allcoupons = []
      
      for (var i=0; i < coupons.length; i++) {
        allcoupons.push({"coupon_id": coupons[i]._id, "code": coupons[i]._id, "value": coupons[i].coupon_value})

        // Read Coupons
        Tts.speak(translations.formatString(translations['couponDetailText'], {coupon_code: coupons[i]._id, currency: translations['currencyLabel'], coupon_value: coupons[i].coupon_value}), 
        {
          androidParams: {
            KEY_PARAM_PAN: -1,
            KEY_PARAM_VOLUME: 0.5,
            KEY_PARAM_STREAM: 'STREAM_MUSIC',
          },
        });
      }

      setCouponsList(allcoupons)
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

  const selectCoupon = function(coupon_id) {

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
                couponsList.map(coupon => {
                  if (coupon.available == 1) {
                    return (
                    <Card
                    style={{display: 'flex', justifyContent: 'space-between', flexDirection: 'row', width: '100%', marginTop: 10}}
                    accessible={true}
                    accessibleRole=""
                    accessibilityLabel={translations.formatString(translations['detailsCouponText'], {coupon_code: coupon.code})}
                    accessibilityHint={translations['detailsCouponText']}
                    onPress={() => selectCoupon(coupon.coupon_id)}
                    // onPress={() => navigation.navigate('orderPending')}
                    >
                    <Card.Content>
                      <View style={{flex: 1, flexDirection: 'row'}}>
                        <View style={{
                            flexGrow: 1,
                        }}>
                        <Title style={{textAlign: 'center'}}>{coupon.code}</Title>
                        <Paragraph style={{textAlign: 'center'}}>
                          <Text style={{fontSize: 18, textAlign: 'center', padding: 10}} accessible={true} accessibilityLabel={translations.formatString(translations['couponValueLabel'], {coupon_code: coupon.code, coupon_value: coupon.value})} accessibilityHint={translations.formatString(translations['couponValueLabelHint'], {coupon_code: coupon.code})}>
                            {translations['currencyLabel']} {coupon.value}{"\n"}
                          </Text>
                        </Paragraph>
                        </View>
                        <View style={{
                          width: 100,
                        }}>      
                          <Paragraph style={{textAlign: 'center'}}>
                            <Text style={{fontSize: 12, textAlign: 'center', padding: 5}} accessible={true} accessibilityLabel={translations.formatString(translations['couponValueLabel'], {coupon_code: coupon.code, coupon_value: coupon.value})} accessibilityHint={translations.formatString(translations['couponValueLabelHint'], {coupon_code: coupon.code})}>
                              {translations['couponApplyText']}
                            </Text>
                          </Paragraph>
                        </View>
                      </View>
                    </Card.Content>
                  </Card>)
                  }
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
                padding: 10,
                marginTop: 20,
                backgroundColor: theme.colors.primary,
                borderRadius: 10,
                alignItems: 'center'
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
