-- Turtle Code --
controller = {
  position = {x=1, y=0, z=1, f=1},
	--We're starting at position 1,1 instead of 0,0
  fuelConsumed = 0,
  blocksTravelled = 0,
  timesRefuelled = 0,
  blocksMined = 0,
	onReturnTrip = false
}
blackList = {
	"minecraft:cobblestone",
	"minecraft:stone",
	"minecraft:bedrock"
}
--Misc functions
function table.contains(table, element)
  for _, value in pairs(table) do
    if value == element then
      return true
    end
  end
  return false
end

--The basic functions do not handle possibilities like unbreakable blocks.
function controller:new(o)
    o = o or {} -- create new object if user does not provide one
    setmetatable(o, self)
    self.__index = self
    return o
end
function controller:up()
	controller:computePositionFromHome()
	if turtle.up() then
   self.position.y = self.position.y+1
	 self.blocksTravelled = self.blocksTravelled+1
	else
		if turtle.detectUp() then
			while turtle.detectUp() do
				controller:digUp()
			end
			turtle.up()
			self.position.y = self.position.y+1
			self.blocksTravelled = self.blocksTravelled+1
		else
			while turtle.up() == false do
				turtle.attackUp()
			end
			self.position.y = self.position.y+1
			self.blocksTravelled = self.blocksTravelled+1
		end
	end
end
function controller:down()
	controller:computePositionFromHome()
	if turtle.down() then
   self.position.y = self.position.y-1
	 self.blocksTravelled = self.blocksTravelled+1
	else
		if turtle.detectDown() then
			while turtle.detectDown() do
				controller:digDown()
			end
			turtle.down()
			self.position.y = self.position.y-1
			self.blocksTravelled = self.blocksTravelled+1
		else
			while turtle.down() == false do
				turtle.attackDown()
			end
			self.position.y = self.position.y-1
			self.blocksTravelled = self.blocksTravelled+1
		end
	end
end
function controller:turnLeft()
	turtle.turnLeft()
	self.position.f = self.position.f-1
	if self.position.f < 1 then
			self.position.f = 4
	end
end
function controller:turnRight()
	turtle.turnRight()
	self.position.f = self.position.f+1
	if self.position.f > 4 then
			self.position.f = 1
	end
end
function controller:forward()
	controller:computePositionFromHome()
	if turtle.forward() == false then
			if turtle.detect() == false then
					while turtle.forward() == false do
							turtle.attack()
					end
			else
					while turtle.forward() == false do
							controller:dig()
					end
			end
	end
	if self.position.f == 1 then
			self.position.z = self.position.z+1 -- North
	elseif self.position.f == 2 then
			self.position.x = self.position.x+1 -- East
	elseif self.position.f == 3 then
			self.position.z = self.position.z-1 -- South
	elseif self.position.f == 4 then
			self.position.x = self.position.x-1 -- West
	end
	self.blocksTravelled = self.blocksTravelled+1
end
function controller:back()
	controller:computePositionFromHome()
	if turtle.back() == false then
			if controller:detectBackward() == false then -- Should turn turtle around 180 degrees
					while turtle.forward() == false do
							turtle.attack()
					end
			else
					while turtle.forward() == false do
							controller:dig()
					end
			end
	end
	turtle.turnRight()
	turlte.turnRight()
	if self.position.f == 1 then
			self.position.z = self.position.z+1 -- North
	elseif self.position.f == 2 then
			self.position.x = self.position.x+1 -- East
	elseif self.position.f == 3 then
			self.position.z = self.position.z-1 -- South
	elseif self.position.f == 4 then
			self.position.x = self.position.x-1 -- West
	end
	self.blocksTravelled = self.blocksTravelled+1
end
function controller:dig()
	if turtle.getItemCount(16) == 0 then
		if turtle.detect() then
			while turtle.detect() do
				turtle.dig()
			end
		end
	else
		controller:consolidateInventory()
		if self.onReturnTrip == false then
			if turtle.getItemCount(16) ~= 0 then
				controller:defaultInventoryFull()
			else
				controller:dig()
			end
		else
			turtle.dig()
		end
	end
	self.blocksMined = self.blocksMined+1
end
function controller:digDown()
	if turtle.getItemCount(16) == 0 then
		if turtle.detectDown() then
			while turtle.detectDown() do
				turtle.digDown()
			end
		end
	else
		controller:consolidateInventory()
		if self.onReturnTrip == false then
			if turtle.getItemCount(16) ~= 0 then
				controller:defaultInventoryFull()
			else
				controller:digDown()
			end
		else
			turtle.digDown()
		end
	end
	self.blocksMined = self.blocksMined+1
end
function controller:digUp()
	if turtle.getItemCount(16) == 0 then
		if turtle.detectUp() then
			while turtle.detectUp() do
				turtle.digUp()
			end
		end
	else
		controller:consolidateInventory()
		if self.onReturnTrip == false then
			if turtle.getItemCount(16) ~= 0 then
				controller:defaultInventoryFull()
			else
				controller:digUp()
			end
		else
			turtle.digUp()
		end
	end
	self.blocksMined = self.blocksMined+1
end
function controller:bedrockSafeDig()
	if turtle.getItemCount(16) == 0 then
		if turtle.detect() then
			_, item = turtle.inspect()
			item = item.name
			if item ~= "minecraft:bedrock" then
				while turtle.detect() do
					turtle.dig()
				end
			else
				return false
			end
		end
	else
		controller:consolidateInventory()
		if turtle.getItemCount(16) ~= 0 then
			controller:defaultInventoryFull()
		else
			controller:dig()
		end
	end
	self.blocksMined = self.blocksMined+1
	return true
end
function controller:bedrockSafeDigUp()
	if turtle.getItemCount(16) == 0 then
		if turtle.detectUp() then
			_, item = turtle.inspectUp()
			item = item.name
			if item ~= "minecraft:bedrock" then
				while turtle.detectUp() do
					turtle.digUp()
				end
			else
				return false
			end
		end
	else
		controller:consolidateInventory()
		if turtle.getItemCount(16) ~= 0 then
			controller:defaultInventoryFull()
		else
			controller:digUp()
		end
	end
	self.blocksMined = self.blocksMined+1
	return true
end
function controller:bedrockSafeDigDown()
	if turtle.getItemCount(16) == 0 then
		if turtle.detectDown() then
			_, item = turtle.inspectDown()
			item = item.name
			if item ~= "minecraft:bedrock" then
				while turtle.detectDown() do
					turtle.digDown()
				end
			else
				return false
			end
		end
	else
		controller:consolidateInventory()
		if turtle.getItemCount(16) ~= 0 then
			controller:defaultInventoryFull()
		else
			controller:digDown()
		end
	end
	self.blocksMined = self.blocksMined+1
	return true
end
function controller:consolidateInventory()
	--Condense all items first.
	if self.onReturnTrip == false then
		for i=1, 16 do
			spaceRemaining = turtle.getItemSpace(i)
			if turtle.getItemDetail(i) then
				itemType = turtle.getItemDetail(i).name
			else
				itemType = nil
			end
			for n=i+1, 16 do
				if turtle.getItemDetail(n) ~= nil then
					if turtle.getItemDetail(n).name == itemType then
						if spaceRemaining > 0 then
							turtle.select(n)
							turtle.transferTo(i)
						end
					end
				end
			end
		end
		turtle.select(1)
		--No reorganize & bring all items to first slots
		for i=1, 16 do
			if turtle.getItemDetail(i) == nil then
				for n=16, i, -1 do
					if turtle.getItemDetail(n) ~= nil then
						turtle.select(n)
						turtle.transferTo(i)
					end
				end
			end
		end
		turtle.select(1)
	end
end
function controller:defaultInventoryFull()
	self.onReturnTrip = true
	returnPos = {x=self.position.x, y=self.position.y, z=self.position.z, f=self.position.f}
	controller:goToPosition(1,0,1,3)
	for i=2, 16 do
		turtle.select(i)
		turtle.drop()
	end
	turtle.select(1)
	required = returnPos.x+returnPos.y+returnPos.z
	if turtle.getFuelLevel() < required then
		readyToGo = false
		while readyToGo == false do
			if (turtle.getFuelLevel() < (required*2)) then
				controller:checkInventoryForFuel()
				os.sleep(1)
			else
				readyToGo = true
			end
		end
	end
	controller:goToPosition(returnPos.x, returnPos.y, returnPos.z, returnPos.f)
	self.onReturnTrip = false
end
function controller:defaultRefuel()
	if controller:checkInventoryForFuel() == true then
		return
	end
	self.onReturnTrip = true
	returnPos = {x=self.position.x, y=self.position.y, z=self.position.z, f=self.position.f}
	controller:goToPosition(1,0,1,3)
	print("No fuel. Returning to surface, and waiting for fuel...")
	required = math.abs(returnPos.x)+math.abs(returnPos.y)+math.abs(returnPos.z)
	readyToGo = false
	while readyToGo == false do
		if (turtle.getFuelLevel() < (required*2)+5) then
			controller:checkInventoryForFuel()
			os.sleep(1)
		else
			readyToGo = true
		end
	end
	print("Returning.")
	controller:goToPosition(returnPos.x, returnPos.y, returnPos.z, returnPos.f)
	self.onReturnTrip = false
end
function controller:computePositionFromHome()
	if self.onReturnTrip == false then
		distance = math.abs(self.position.x)+math.abs(self.position.y)+math.abs(self.position.z)-2
		if (distance+5) > turtle.getFuelLevel() then
				controller:defaultRefuel()
		else
			return
		end
	end
end
function controller:goToPosition(x, y, z, f)
	print("Navigating to x:"..x.." y:"..y.." z:".." "..z.." f:"..f)
	if self.onReturnTrip == false then
		fuelToGetToPosition = math.abs(x)+math.abs(y)+math.abs(z)
		if (turtle.getFuelLevel() < (fuelToGetToPosition*2)) then
			for i=1, 16 do
				turtle.select(i)
				turtle.refuel(2)
			end
			turtle.select(1)
			if (turtle.getFuelLevel() < (fuelToGetToPosition*2)) then
				print("I need more fuel to continue!")
				while (turtle.getFuelLevel() < (fuelToGetToPosition*2)) do
					controller:checkInventoryForFuel()
					os.sleep(1)
				end
			end
		end
	end
	if x > self.position.x then
		while self.position.f ~= 2 do
			controller:turnRight()
		end
		while x > self.position.x do
			controller:forward()
		end
	elseif x < self.position.x then
		while self.position.f ~= 4 do
			controller:turnRight()
		end
		while x < self.position.x do
			controller:forward()
		end
	end

	if z > self.position.z then
		while self.position.f ~= 1 do
			controller:turnRight()
		end
		while z > self.position.z do
			controller:forward()
		end
	elseif z < self.position.z then
		while self.position.f ~= 3 do
			controller:turnRight()
		end
		while z < self.position.z do
			controller:forward()
		end
	end
	if y > self.position.y then
		while y > self.position.y do
			controller:up()
		end
	elseif y < self.position.y then
		while y < self.position.y do
			controller:down()
		end
	end

	while f ~= self.position.f do
		controller:turnRight()
	end
end
function controller:bedrockSafeColumn(x, z)
	startY = self.position.y
	controller:goToPosition(x, self.position.y, z, self.position.f)
	canContinue = true
	threshhold = 5
	while canContinue do
		if turtle.detectDown() then
			if controller:bedrockSafeDigDown() == false then
				for i=0, threshhold do
					controller:bedrockSafeDig()
				end
				if turtle.detectDown() == false then
					controller:down()
				else
					canContinue = false
				end
			else
				controller:down()
			end
		else
			controller:down()
		end
		--Assume has gone down now
		for i=0, 3 do
			controller:turnRight()
			if turtle.inspect() then
				_, item = turtle.inspect()
				item = item.name
				if table.contains(blackList, item) == false then
					controller:dig()
				end
			end
		end
	end
	controller:goToPosition(x, startY, z, self.position.f)
end
function controller:detectBackward()
	controller:turnRight()
	controller:turnRight()
	val = turtle.detect()
	controller:turnLeft()
	controller:turnLeft()
	return val
end

function controller:emptyInventory()
	for i=1, 16 do
		turtle.select(i)
		turtle.drop()
	end
	turtle.select(1)
end
function controller:checkInventoryForFuel()
	for i=1, 16 do
		turtle.select(i)
		if turtle.refuel(1) == true then
			turtle.select(1)
			return true
		end
	end
	turtle.select(1)
	return false
end


--Digging Algo--
me = controller:new()
maxx = 8
maxz = 8
for x=1, maxx do
	for z=1, maxz do
		if z%2 == 1 then
			if ((x+2)%4) == 0 then
				controller:bedrockSafeColumn(x, z)
			end
		else
			if (x%4) == 0 then
				controller:bedrockSafeColumn(x, z)
			end
		end
	end
end
controller:goToPosition(1, 0, 1, 3)
print("All done :)")
print("Mined items: "..me.blocksMined)
print("Fuel consumed: "..me.blocksTravelled)
