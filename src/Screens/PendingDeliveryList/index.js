/* eslint-disable react-native/no-inline-styles */
import React, {useState, useContext, useEffect} from 'react';
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
import { Avatar, Button, Card, Title, Paragraph } from 'react-native-paper';
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
  const [pendingOrdersList, setPendingOrdersList] = useState([])

  const LISTEN_COMMAND_EN = "begin"
  const LISTEN_COMMAND_TA = "தொடங்க"
  
  const {
    translations
  } = useContext(LocalizationContext);

  const createData = () => {
    var orders = []
    orders.push({"order_id":1,"shop_id":1,"shop_name":"Taniya","user_id":1,"coupon_id":1,"coupon_code":"CV100", "coupon_value":100, "order_status":0,"order_payment":0,"items":
                                                                                              [{"item_id":1,"item_name":"Rice","item_code":"Rice001","item_rate":100,"item_offer_price":90,"item_qty":1},
                                                                                              {"item_id":2,"item_name":"Sugar","item_code":"Sugar001","item_rate":200,"item_offer_price":null,"item_qty":1}]})
    orders.push({"order_id":2,"shop_id":2,"shop_name":"Wijesekara","user_id":1,"coupon_id":null,"order_status":0,"order_payment":1,"items":{"item_id":2,"item_name":"Sugar","item_code":"Sugar001","item_rate":200,"item_offer_price":null,"item_qty":1}})
    orders.push({"order_id":3,"shop_id":1,"shop_name":"Taniya","user_id":1,"coupon_id":null,"order_status":0,"order_payment":0,"items":{"item_id":2,"item_name":"Sugar","item_code":"Sugar001","item_rate":200,"item_offer_price":null,"item_qty":1}})
    orders.push({"order_id":4,"shop_id":2,"shop_name":"Wijesekara","user_id":1,"coupon_id":null,"order_status":0,"order_payment":0,"items":{"item_id":1,"item_name":"Rice","item_code":"Rice001","item_rate":100,"item_offer_price":null,"item_qty":1}})
    orders.push({"order_id":5,"shop_id":2,"shop_name":"Wijesekara","user_id":1,"coupon_id":null,"order_status":0,"order_payment":0,"items":{"item_id":1,"item_name":"Rice","item_code":"Rice001","item_rate":100,"item_offer_price":null,"item_qty":1}})
    orders.push({"order_id":6,"shop_id":2,"shop_name":"Wijesekara","user_id":1,"coupon_id":null,"order_status":0,"order_payment":0,"items":{"item_id":1,"item_name":"Rice","item_code":"Rice001","item_rate":100,"item_offer_price":null,"item_qty":1}})
    
    setPendingOrdersList(orders)
  }

  const getData = async () => {
    try {
      var allOrders=[]
      const orders = await AsyncStorage.getItem('@allorders');

      for (var i=0; i<orders.length; i++) {
        if (orders[i].order_status == 0) {
          allOrders.push({"order_id": orders[i].order_id, "shop_id": orders[i].shop_id, "shop_name": orders[i].shop_name, "coupon_id": orders[i].coupon_id, "coupon_code": orders[i].coupon_code, "coupon_value": orders[i].coupon_value, "order_status": orders[i].order_status, "order_payment": orders[i].order_payment, "items": orders[i].items})
        }
      }

      setPendingOrdersList(allOrders)
    } catch (e) {
      console.log('ee');
    }
  }

  useEffect(() => {
    getData()
    Voice.onSpeechStart = onSpeechStart()
    Voice.onSpeechRecognized = onSpeechRecognized()
    Voice.onSpeechResults = onSpeechResults()

    var msg="";
    // Iterate Pending Orders and Create a Message to Read
    for (var i = 0; i < pendingOrdersList.length; i++) {
      var itms = pendingOrdersList[i].items;
      var total=0;
      for (var j=0; j < itms.length; j++) {
        if (itms[j].item_offer_price != null) {
          total += itms[j].item_offer_price;
        }
      }

      msg+=translations.formatString(translations['orderDetailInfo'], {order_id: pendingOrdersList[i].order_id, shop_name: pendingOrdersList[i].shop_name, currency: translations['currencyLabel'], total: total, length: itms.length});
    }

    console.log(msg)
    // Tts.setDefaultLanguage('ta-IN');
    Tts.setDefaultLanguage('en-IN');
    Tts.speak(
      translations['pendingOrdersLisTts']+msg,
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
      if (menuitem.includes("order")) {
        var list = menuitem.split('order')
        for(var i =0; i < list.length; i++) {
          if (!isNaN(list[i])) {
            // Is a Number
            console.log("Order Number: "+list[i])
            for (var i=0; i < pendingOrdersList.length; i++) {
              if (pendingOrdersList[i].order_id == list[i]) {
                // matching order

                navigation.navigate('orderCancelled', pendingOrdersList[i])
              }
            }
          }
        }
      } else if (menuitem.includes("ஒர்டெர்")) {
        var list = menuitem.split('ஒர்டெர்')
        for(var i =0; i < list.length; i++) {
          if (!isNaN(list[i])) {
            // Is a Number
            console.log("Order Number: "+list[i])
            for (var i=0; i < pendingOrdersList.length; i++) {
              if (pendingOrdersList[i].order_id == list[i]) {
                // matching order

                navigation.navigate('orderCancelled', pendingOrdersList[i])
              }
            }
          }
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

  const viewOrder = function (id) {
    // Take the User to Order View Screen
    navigation.navigate('orderPending', id)
  }

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
        if (!response.flag === 'navigation-error') {
          navigation.navigate(response.flag);
        } else {
          console.log('route error');
        }
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
                  pendingOrdersList.map(order => {
                    var total=0;
                    for (var i=0; i < order.items.length; i++) {
                      if (order.items[i].item_offer_price != null) {
                        total += order.items[i].item_offer_price * order.items[i].item_qty
                      } else {
                        total += order.items[i].item_rate * order.items[i].item_qty
                      }
                    }

                    return (
                    <Card
                    style={{display: 'flex', justifyContent: 'space-between', flexDirection: 'row', width: '100%', marginTop: 10}}
                    accessible={true}
                    accessibleRole=""
                    accessibilityLabel={translations.formatString(translations['orderDetailText'], {order_id: order.order_id})}
                    accessibilityHint={translations.formatString(translations['orderDetailHint'], {order_id: order.order_id})}
                    onPress={() => navigation.navigate('orderPending', order.order_id)}
                    // onPress={() => navigation.navigate('orderPending')}
                    key={order.order_id}
                    >
                      <Card.Content>
                        <View style={{flex: 1, flexDirection: 'row'}}>
                          <View style={{
                                flexGrow: 0.1,
                                justifyContent: 'center'
                            }}>
                              <IconX
                                style={{margin: 5}}
                                origin={ICON_TYPE.FONT_AWESOME}
                                name={'info'}
                                color={theme.colors.primary}
                              />
                          </View>
                          <View style={{
                            flexGrow: 0.5,
                            padding: 5
                          }}>
                            <Paragraph style={{textAlign:'left'}}>
                              <Text style={{fontSize: 16, textTransform: 'capitalize'}} accessible={true} accessibilityLabel={translations.formatString(translations['orderDetailText'], {order_id: order.order_id})} accessibilityHint={translations.formatString(translations['orderDetailHint'], {order_id: order.order_id})} accessibilityRole="text">
                                {translations["indvOrderLabel"]} #{order.order_id}{"\n"}
                              </Text>
                              <Text style={{fontSize: 12, textTransform: 'capitalize'}} accessible={true} accessibilityLabel={translations.formatString(translations['shopDetailText'], {shop_name: order.shop_name})} accessibilityHint={translations.formatString(translations['shopDetailHint'], {shop_name: order.shop_name})} accessibilityRole="text">
                                {translations["shopLabel"]}: {order.shop_name}{"\n"}
                                {order.coupon_id != null ? 
                                <Text style={{fontSize: 12, textAlign: 'center', padding: 10}} accessible={true} accessibilityLabel={translations.formatString(translations['couponDetailText'], {coupon_code: order.coupon_code, currency: translations['currencyLabel'], coupon_value: order.coupon_value})} accessibilityHint={translations.formatString(translations['couponDetailHint'], {coupon_code: order.coupon_code, currency: translations['currencyLabel'], coupon_value: order.coupon_value})} accessibilityRole="text">
                                  {translations["couponLabel"]}: {order.coupon_code} - Rs.{order.coupon_value}{"\n"}
                                </Text>
                                : translations["couponLabel"]+": N/A\n"}
                              </Text>
                              <Text style={{fontSize: 14, textAlign: 'center', padding: 10}} accessible={true} accessibilityLabel={translations.formatString(translations['orderItemDetailText'], {length: order.items.length})} accessibilityHint={translations.formatString(translations['orderItemDetailHint'], {length: order.items.length, order_id: order.order_id, shop_name: order_id.shop_name})} accessibilityRole="text">
                                {translations['totalAmountLabel']}: {translations['currencyLabel']} {total}{"\n"}
                              </Text>
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
            style={{ width: '100%' }}
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
