/* eslint-disable react-native/no-inline-styles */
import React, {useContext, useEffect, useState} from 'react';
import {View, Text, SafeAreaView, ScrollView} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {Container, HeaderButton} from '../../Components';
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
import { Avatar, Button, Card, Title, Paragraph } from 'react-native-paper';
import { LocalizationContext } from '../../Translations';
import { Voice } from '@react-native-voice/voice';

const MainScreen = ({routes, route, navigation}) => {
  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {response} = route.params;
  const [resList, setListData] = useState('');
  const [order, setOrder] = useState(null);
  const [total, setTotal] = useState(0);
  
  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"

  const { translations } = useContext(LocalizationContext)
  
  useEffect(() => {
    createData()
    Voice.onSpeechStart = onSpeechStart()
    Voice.onSpeechRecognized = onSpeechRecognized()
    Voice.onSpeechResults = onSpeechResults()

    Tts.speak("You are viewing Order #1", {
      androidParams: {
        KEY_PARAM_PAN: -1,
        KEY_PARAM_VOLUME: 0.5,
        KEY_PARAM_STREAM: 'STREAM_MUSIC',
      },
    });
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
    setOrder({"order_id":1,"shop_id":1,"shop_name":"Taniya","user_id":1,"coupon_id":1,"coupon_code":"CV100", "coupon_value":100, "order_status":0,"order_payment":0,"items":
    [{"item_id":1,"item_name":"Rice","item_code":"Rice001","item_rate":"100","item_offer_price":null,"item_qty":1,"item_unit":"kg"},
    {"item_id":2,"item_name":"Sugar","item_code":"Sugar001","item_rate":"200","item_offer_price":null,"item_qty":2,"item_unit":"kg"}]})
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

  const markReceived = () => {
    navigation.navigate('markReceived', order.order_id);
  }

  const markCancelled = () => {
    navigation.navigate('markCancelled', order.order_id);
  }

  const markReturned = () => {
    navigation.navigate('markReturned', order.order_id);
  }

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
              padding: 10,
            }}>

              { 
              order ? 
              <>
                <Title>{translations.formatString(translations['orderDetailText'], {order_id: order.order_id})}</Title>
                <Card style={{backgroundColor: 'transparent', borderColor: '#ccc', margin: 10}} accessible={true} accessibilityLabel={`Viewing Order ${order.order_id}`} accessibilityHint={`You are Viewing Order #${order.order_id} and the items that the order contains`}>
                  <Card.Content>
                    <Paragraph>
                      <Text>
                        {translations['shopLabel']}: {order.shop_name}{"\n"}
                        {translations['couponLabel']}: {order.coupon_id != null ? order.coupon_code + " - "+translations['currencyLabel']+"." + order.coupon_value : "None"}{"\n"}
                        {translations['paymentMethodLabel']}: {order.order_payment == 0 ? "Cash On Delivery" : "Card"}{"\n"}
                        {translations['orderStatusLabel']}: Pending{"\n"}
                      </Text>
                    </Paragraph>
                  </Card.Content>                  
                </Card>

                {order.items.map(item => {
                  var totalLocal=0;
                  if (item.item_offer_price != null) {
                    totalLocal += item.item_offer_price * item.item_qty
                  } else {
                    totalLocal += item.item_rate * item.item_qty
                  }

                  return (
                    <Card style={{margin: 10}} accessible={true} accessibility={`Item ${item.item_name}`} accessibilityHint={`Item ${item.item_name}, Quantity ${item.item_qty}, Price Rs.${item.item_offer_price != null ? item.item_offer_price : item.item_rate}, Rs.Total ${item.item_offer_price != null ? item.item_offer_price*item.item_qty : item.item_rate*item.item_qty}`} accessibilityRole="text">
                      <Card.Content>
                        <Text style={{fontSize: 14, fontWeight: '800', textAlign: 'left', margin: 0, padding: 0}} accessible={true} >
                          {item.item_name}
                        </Text>
                        <Text style={{fontSize: 12}}>
                          {item.item_qty}{item.item_unit}{"\n"}
                          {item.item_offer_price != null ? translations['itemPriceOfferLabel']+": "+translations['currencyLabel']+"."+item.item_offer_price : translations['itemPriceLabel']+": "+translations['currencyLabel']+"."+item.item_rate}{"\n"}
                          {item.item_offer_price != null ? translations['totalAmountLabel']+": "+translations['currencyLabel']+"."+(item.item_offer_price*item.item_qty) : translations['totalAmountLabel']+": "+translations['currencyLabel']+"."+(item.item_rate*item.item_qty)}{"\n"}
                        </Text>
                      </Card.Content>
                    </Card>
                  )
                })}

                {/* <Card accessible={true} accessibilityLabel={`Total Amount Rs.${total}`} accessibilityHint={`The Total Order Amount for all the items is Rs.${total}`}>
                  <Card.Content>
                    <Text style={{fontSize: 14}}>Total: Rs.500</Text>{"\n"}
                  </Card.Content>
                </Card> */}
              </>
              : 
              <Text>Order Loading</Text>}
          </View>

          <View style={{flex: 1, flexDirection: 'column', justifyContent: 'space-evenly'}}>
            <View style={{flexGrow: 1}}>
              <ButtonX
                accessible={true}
                accessibilityLabel={translations['markReceivedTitle']}
                accessibilityRole="button"
                dark={true}
                color={theme.colors.primary}
                label={translations['markReceivedTitle']}
                onPress = {() => Tts.speak(translations.formatString(translations['markReceivedLongPress'], {order_id: order.order_id}))}
                onLongPress={() => navigation.navigate('markReceived',order.order_id)}
              />
            </View>
            <View style={{flexGrow: 1}}>
              <ButtonX
                accessible={true}
                accessibilityLabel={translations['markReturnedTitle']}
                accessibilityRole="button"
                dark={true}
                color={theme.colors.primary}
                label={translations['markReturnedTitle']}
                onPress = {() => Tts.speak(translations.formatString(translations['markReturnedLongPress'], {order_id: order.order_id}))}
                onLongPress={() => navigation.navigate('markReturned',order.order_id)}
              />
            </View>
            <View style={{flexGrow: 1}}>
              <ButtonX
                accessible={true}
                accessibilityLabel={translations['markCancelledTitle']}
                accessibilityRole="button"
                dark={true}
                color={theme.colors.primary}
                label={translations['markCancelledTitle']}
                onPress = {() => Tts.speak(translations.formatString(translations['markCancelledLongPress'], {order_id: order.order_id}))}
                onLongPress={() => navigation.navigate('markCancelled',order.order_id)}
              />
            </View>
            <View style={{flexGrow: 1}}>
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
          </View>
        </ScrollView>
      </SafeAreaView>
    </LoadingActionContainer>
  );
};
export default MainScreen;
