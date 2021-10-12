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
import {ButtonX} from '../../Components';
import AudioRecord from 'react-native-audio-record';
import {BASE_URL} from '../../Config/index';

const MainScreen = ({routes, navigation}) => {
  const {theme} = useAppTheme();
  // eslint-disable-next-line prettier/prettier
  const {username, password} = useStoreState((state) => ({
    username: state.login.username,
    password: state.login.password,
  }));

  useEffect(() => {
    const _toggleDrawer = () => {
      navigation.toggleDrawer();
      fetchProducts();
      const options = {
        sampleRate: 16000, // default 44100
        channels: 1, // 1 or 2, default 1
        bitsPerSample: 16, // 8 or 16, default 16
        audioSource: 6, // android only (see below)
        wavFile: 'test.wav', // default 'audio.wav'
      };

      AudioRecord.init(options);
    };

    console.log('use effect home');
  }, [navigation, theme.colors.headerTitle]);
  const fetchProducts = () => {
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
      // .then((response) => response.json())
      .then((response) => {
        console.log('response 🤡🤡');
        console.log(response);
      })
      .catch((err) => console.error(err));
  };
  const names = ['Bruce', 'Clark', 'Diana'];

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
        <View
          style={{
            flex: 1,
            flexDirection: 'column',
            justifyContent: 'space-around',
          }}>
          <ButtonX
            // loading={loading}
            dark={true}
            color={theme.colors.primary}
            onPress={() => navigation.navigate('order-pending')}
            label={'Create Product List'}
          />
          <View
            style={{
              flex: 1,
              flexDirection: 'row',
              justifyContent: 'space-around',
            }}>
            <View>
              <InputX
                label="Product Name"
                // mode="outlined"
                // ref={inputUserName}
                style={{marginTop: 10, backgroundColor: '#fafafa', width: 200}}
                autoCapitalize="none"
                returnKeyType={'next'}
                // onSubmitEditing={onSubmit}
                // onChangeText={(text) =>
                //   onChange({
                //     key: 'username',
                //     value: text,
                //   })
                // }
              />
            </View>
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

              {names.map((name) => (
                <Text>{name}</Text>
              ))}
            </View>
            <View
              style={{
                flex: 1,
                // flexDirection: 'column',
                justifyContent: 'space-around',
              }}>
              <Text>QTY</Text>
              {names.map((name) => (
                <Text>1</Text>
              ))}
            </View>
            <View
              style={{
                flex: 1,
                // flexDirection: 'column',
                justifyContent: 'space-around',
              }}>
              <Text>Action</Text>
              {names.map((name) => (
                <Text>1</Text>
              ))}
            </View>
          </View>
          <ButtonX
            // loading={loading}
            dark={true}
            color={theme.colors.primary}
            onPress={() => navigation.navigate('ProductList')}
            label={'Create'}
          />
        </View>
      </Container>
    </LoadingActionContainer>
  );
};

export default MainScreen;
