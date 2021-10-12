/* eslint-disable react-native/no-inline-styles */
import React, {useEffect, useState} from 'react';
import {View, Text} from 'react-native';
import LoadingActionContainer from '../../Components/LoadingActionContainer';
import {Container, HeaderButton, InputX} from '../../Components';
import useAppTheme from '../../Themes/Context';
import {IconX, ICON_TYPE} from '../../Icons';
import {useStoreState} from 'easy-peasy';
import Fonts from '../../Themes/Fonts';
import {TouchableOpacity, ListItem} from 'react-native';
import AudioRecord from 'react-native-audio-record';
import {BASE_URL} from '../../Config/index';
import AsyncStorage from '@react-native-community/async-storage';
import Tts from 'react-native-tts';

import {ButtonX} from '../../Components';
const MainScreen = ({routes, route, navigation}) => {
  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {response} = route.params;
  useEffect(() => {
    console.log('🌙🌙', response);
    const newData = JSON.parse(response.cartitems);
    for (let value of newData) {
      // for (let value of searchData.list) {
      Tts.speak(`item`, {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      });
      Tts.speak(value.item_name, {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      });
      const myNumber = value.item_qty;
      var myString = myNumber.toString();

      Tts.speak(myString, {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      });
      Tts.speak('kilograms', {
        androidParams: {
          KEY_PARAM_PAN: -1,
          KEY_PARAM_VOLUME: 0.5,
          KEY_PARAM_STREAM: 'STREAM_MUSIC',
        },
      });
    }
    setResData(newData);
    console.log('😎', newData);
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

    console.log('use effect home');
  }, [navigation, theme.colors.headerTitle]);
  const [resData, setResData] = useState('');

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
    console.log('🧑‍🚀🧑‍🚀', fileUrl);
    let formData = new FormData();
    formData.append('audioFile', {
      uri: 'file:///data/user/0/com.easy_boiler/files/test.wav',
      type: 'audio/wav',
      name: 'test.wav',
    });
    formData.append('flag', 'name');
    formData.append('userId', 3);
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
        console.log('response 🔥🔥🔥', response.flag);
        console.log(response);
        // if (!response.flag === 'navigation-error') {
        //   navigation.navigate(response.flag);
        // } else {
        //   console.log('route error');
        // }
        if (response.flag == 'back') {
          navigation.navigate('language-success');
        }
        if (response.flag == 'place-order') {
          navigation.navigate('place-order', {
            response,
          });
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
        if (response.flag == 'search-save') {
          navigation.navigate('search-save', {
            response,
          });
        }
        if (response.flag == 'check-order') {
          // navigation.navigate('check-order');
        }
      })

      .catch((err) => console.error(err));
  };

  const postData = () => {
    const requestOptions = {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        data: [
          {
            itemname: 'banana',
            itemqty: 1,
          },
          {
            itemname: 'apple',
            itemqty: 2,
          },
        ],
        userId: 3,
      }),
    };
    fetch(`${BASE_URL}/ocr/search`, requestOptions)
      .then((response) => response.json())
      .then((data) => resposeTTS(data));
  };
  const resposeTTS = (data) => {
    console.log(data);
    Tts.speak(data.msg, {
      androidParams: {
        KEY_PARAM_PAN: -1,
        KEY_PARAM_VOLUME: 0.5,
        KEY_PARAM_STREAM: 'STREAM_MUSIC',
      },
    });
    navigation.navigate('OCROrderConfirm', resData);
  };
  const [resList, setListData] = useState('');
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
          <View
            style={{
              flex: 1,
              flexDirection: 'row',
              justifyContent: 'center',
              backgroundColor: '#e1e1e1',
            }}>
            <View
              style={{
                flex: 1,
                // flexDirection: 'column',
                justifyContent: 'space-around',
                paddingLeft: 20,
              }}>
              <Text>Name</Text>

              {resData
                ? resData.map((item) => <Text> {item.item_name} </Text>)
                : null}
            </View>
            <View
              style={{
                flex: 1,
                // flexDirection: 'column',
                justifyContent: 'space-around',
              }}>
              <Text>QTY</Text>
              {resData
                ? resData.map((item, i) => (
                    <Text name="item_qty">{item.item_qty}</Text>
                  ))
                : null}
            </View>
            <View
              style={{
                flex: 1,
                // flexDirection: 'column',
                justifyContent: 'space-around',
              }}>
              <Text>item unit</Text>
              {resData
                ? resData.map((item) => <Text> {item.item_qty} </Text>)
                : null}
            </View>
          </View>

          <View
            style={{
              flex: 1,
              flexDirection: 'row',
              justifyContent: 'space-around',
            }}>
            <View style={{alignItems: 'center'}}>
              <TouchableOpacity onPress={record}>
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
            <View style={{alignItems: 'center'}}>
              <TouchableOpacity>
                <View
                  style={{
                    padding: 10,
                    marginTop: 20,
                    backgroundColor: theme.colors.primary,
                    borderRadius: 10,
                  }}>
                  <IconX name={'md-add'} style={{color: '#fff'}} />
                </View>
              </TouchableOpacity>
            </View>
          </View>
          <ButtonX
            // loading={loading}
            dark={true}
            color={theme.colors.primary}
            onPress={() => postData()}
            label={'Place Order'}
          />
          {/* <ButtonX
            // loading={loading}
            dark={true}
            color={theme.colors.primary}
            // onPress={() => navigation.navigate('OCROrderConfirm', resData)}
            label={'Place Order'}
          /> */}
        </View>
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
