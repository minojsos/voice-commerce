/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useContext, useState} from 'react';
import {View, Text, SafeAreaView, ScrollView} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {Container, HeaderButton, InputX} from '../../Components';
import useAppTheme from '../../Themes/Context';
import {IconX, ICON_TYPE} from '../../Icons';
import {useStoreState} from 'easy-peasy';
import Fonts from '../../Themes/Fonts';
import {TouchableOpacity} from 'react-native';
import {ButtonX} from '../../Components';
import metrics from '../../Themes/Metrics';
import {Image} from 'react-native';
import AudioRecord from 'react-native-audio-record';
import {BASE_URL} from '../../Config/index';
import Tts from 'react-native-tts';
import { LocalizationContext } from '../../Translations';
import { Card, Paragraph, Title } from 'react-native-paper';
import { Voice } from '@react-native-voice/voice';
import AsyncStorage from '@react-native-community/async-storage';

const MainScreen = ({routes, route, navigation}) => {
  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {response} = route.params;
  const [order, setOrder] = useState(null);
  const [reviewOrder, setReviewOrder] = useState('');

  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"

  const {
    translations
  } = useContext(LocalizationContext);
  
  const createData = () => {
    setOrder({"order_id":1,"shop_id":1,"shop_name":"Taniya","user_id":1,"coupon_id":1,"coupon_code":"CV100", "coupon_value":100, "order_status":0,"order_payment":0,"items":
    [{"item_id":1,"item_name":"Rice","item_code":"Rice001","item_rate":"100","item_offer_price":null,"item_qty":1},
    {"item_id":2,"item_name":"Sugar","item_code":"Sugar001","item_rate":"200","item_offer_price":null,"item_qty":1}]})
  }

  useEffect(() => {
    createData()
    Voice.onSpeechStart = onSpeechStart()
    Voice.onSpeechRecognized = onSpeechRecognized()
    Voice.onSpeechResults = onSpeechResults()

    Tts.speak(translations.formatString(translations['markOrderCancelledTts'], {order_id: 1}), 
      { 
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        }
      }
    )

    // console.log('hello ', JSON.parse(response.orders));
    // Tts.speak(response.msg, {
    //   androidParams: {
    //     KEY_PARAM_PAN: -1,
    //     KEY_PARAM_VOLUME: 0.5,
    //     KEY_PARAM_STREAM: 'STREAM_MUSIC',
    //   },
    // });
    // const newData = JSON.parse(response.orders);
    // setListData(newData);
    // for (let value of newData) {
    //   // for (let value of searchData.list) {
    //   Tts.speak(`address${value.address}`, {
    //     androidParams: {
    //       KEY_PARAM_PAN: -1,
    //       KEY_PARAM_VOLUME: 0.5,
    //       KEY_PARAM_STREAM: 'STREAM_MUSIC',
    //     },
    //   });
    //   // Tts.speak(`cancel_reason${value.cancel_reason}`, {
    //   //   androidParams: {
    //   //     KEY_PARAM_PAN: -1,
    //   //     KEY_PARAM_VOLUME: 0.5,
    //   //     KEY_PARAM_STREAM: 'STREAM_MUSIC',
    //   //   },
    //   // });
    // }
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
  }, []);

  const saveReviewOrder = () => {
    if (reviewOrder != "") {

    }
  }

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
      if (menuitem.includes("cancel")) {
        var list = menuitem.split('cancel')
        if (list.length > 1 && list[1] != "") {
          var reason = list[1]
          let formdata = FormData()
          // formdata.append('userId', await AsyncStorage.getItem('userId'))
          formdata.append('orderId', order.order_id)
          formdata.append('feedback',list[1])
          console.log("Reason: "+list[1])

          fetch(`${BASE_URL}/canceled`, {
            method: 'POST',
            headers: {
              'Content-Type': 'multipart/form-data',
            },
            body: formData,
          })
            .then((response) => response.json())
            .then((response) => {
              Tts.speak(translations['successCancelled'])
              navigation.navigate('assistant')
            })
            .catch((err) => console.error(err));
        }
      } else if (menuitem.includes("ரத்து")) {
        var list = menuitem.split('ரத்து')
        if (list.length > 1 && list[1] != "") {
          var reason = list[1]
          let formdata = FormData()
          // formdata.append('userId', await AsyncStorage.getItem('userId'))
          formdata.append('orderId', order.order_id)
          formdata.append('feedback',list[1])
          console.log("Reason: "+list[1])

          fetch(`${BASE_URL}/canceled`, {
            method: 'POST',
            headers: {
              'Content-Type': 'multipart/form-data',
            },
            body: formData,
          })
            .then((response) => response.json())
            .then((response) => {
              Tts.speak(translations['successCancelled'])
              navigation.navigate('assistant')
            })
            .catch((err) => console.error(err));
        }
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
    formData.append('flag', 'name');
    formData.append(orderId, 1);
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
          Tts.speak(response.msg, {
            androidParams: {
              KEY_PARAM_PAN: -1,
              KEY_PARAM_VOLUME: 0.5,
              KEY_PARAM_STREAM: 'STREAM_MUSIC',
            },
          });
          navigation.navigate('order-menu');
        }
        if (!response.flag === 'navigation-error') {
          navigation.navigate(response.flag);
        } else {
          console.log('route error');
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

  return (
    <LoadingActionContainer fixed>
      <SafeAreaView
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

              { order != null ?
              <>
                <Card accessible={true} accessibilityLabel={translations.formatString(translations['viewOrderText'], {order_id: order.order_id})} accessibilityHint={translations.formatString(translations['cancelOrderTextHint'], {order_id: order.order_id})}>
                  <Card.Content>
                    <Title>{translations.formatString(translations['cancelOrderText'], {order_id: order.order_id})}</Title>
                    <InputX
                      multiline={true}
                      numberOfLines={4}
                      accessible={true}
                      label={translations['cancelLabel']}
                      accessibilityLabel={translations['cancelLabel']}
                      accessibilityHint={translations.formatString(translations['cancelHint'], {order_id: order.order_id})}
                      style={{backgroundColor: '#fafafa'}}
                      autoCapitalize="none"
                      returnKeyType={'next'}
                      onChangeText={setReviewOrder}
                      value={reviewOrder}
                  />

                  <ButtonX
                      label={translations['confirmLabel']}
                      accessible={true}
                      accessibilityLabel={translations['confirmLabel']}
                      accessibilityHint={translations.formatString(translations['confirmCancelHint'], {order_id: order.order_id})}
                      accessibilityRole="button"
                      dark={true}
                      color={theme.colors.primary}
                      onPress={saveReviewOrder}
                  />
                  
                  <ButtonX
                      label={translations['cancelLabel']}
                      accessible={true}
                      accessibilityLabel={translations['cancelLabel']}
                      accessibilityHint={translations['cancelButtonHint']}
                      accessibilityRole="button"
                      dark={true}
                      color={theme.colors.primary}
                  />
                  </Card.Content>                  
                </Card>
              </>
              : 
              <Text>Order Loading</Text>}
              
          </View>
          
        </ScrollView>

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
      </SafeAreaView>
    </LoadingActionContainer>
  );
};
export default MainScreen;
