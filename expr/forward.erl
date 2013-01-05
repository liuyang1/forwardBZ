-module(forward).
-export([start/0,client/1,forward/0,front/0,timing/0,forwardloop/1,frontloop/2]).

-define(inport,1234).
-define(outport,1235).

start() ->
	register(forwarder,spawn(forward,forward,[])),
	register(fronter,spawn(forward,front,[])),
	register(timer,spawn(forward,timing,[])).

forward() ->
	{ok,InSocket} = gen_udp:open(?inport,[binary]),
	forwardloop(InSocket).

forwardloop(InSocket) ->
	receive
		{udp,InSocket,_,_,Bin} ->
			fronter ! {dataflow,Bin},
			forwardloop(InSocket)
	end.

front() ->
	{ok,OutSocket}= gen_udp:open(?outport,[binary]),
	frontloop(OutSocket,[]).

frontloop(OutSocket,Addrlist) ->
	receive
		{udp,OutSocket,Host,Port,_} ->
			frontloop(OutSocket,addAddrlist(Addrlist,{Host,Port}));
		{dataflow,Bin} ->
			sendAddrlist(Addrlist,OutSocket,Bin),
			frontloop(OutSocket,Addrlist);
		{timer} ->
			frontloop(OutSocket,incTTL(Addrlist))
	end.

timing() ->
	receive
		_->io:format("heart mass~n")
	after 1000->
		fronter ! {timer},
		timing()
end.

sendAddrlist([],_,_)-> ok;
sendAddrlist(Lst,OutSocket,Bin)->
	[{{Host,Port},_}|Tail]=Lst,
	gen_udp:send(OutSocket,Host,Port,Bin),
	sendAddrlist(Tail,OutSocket,Bin).

addAddrlist([],Addr)-> [{Addr,0}];
addAddrlist([{HAddr,HTTL}|T],Addr)->
	if 
		HAddr==Addr -> [{HAddr,0}|T];
		true -> [{HAddr,HTTL}|addAddrlist(T,Addr)]
	end.

incTTL([])->[];
incTTL([{Addr,TTL}|T])->
	if
		TTL>=20 -> incTTL(T);
		true -> [{Addr,TTL+1}|incTTL(T)]
	end.
%%% simulator client
client(N) ->
	{ok,Socket} = gen_udp:open(0,[binary]),
	io:format("client open socket ~p~n",[Socket]),
	ok = gen_udp:send(Socket,"localhost",1234,N),
	Value = receive
		{udp,Socket,_,_,Bin} ->
			io:format("client rece: ~p~n",[Bin])
		after 2000 ->
			0
	end,
	gen_udp:close(Socket),
	Value.
