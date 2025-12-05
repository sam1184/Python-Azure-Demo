# ============================================================================
# LAB 5: AZURE RESOURCE MANAGER WITH OOP
# Topics: Object-Oriented Programming, Classes, Inheritance, Encapsulation
# ============================================================================

# ============================================================================
# CELL 1: Base Classes - Inheritance Fundamentals
# ============================================================================
from datetime import datetime
from abc import ABC, abstractmethod
import random

print("=" * 70)
print("🏗️  AZURE RESOURCE MANAGER - OOP LAB")
print("=" * 70)

class AzureResource(ABC):
    """
    Abstract base class for all Azure resources
    Demonstrates: Inheritance, Encapsulation, Abstract Methods
    """
    
    # Class variable (shared by all instances)
    total_resources = 0
    
    def __init__(self, name, resource_group, location, tags=None):
        # Instance variables (encapsulation - private data)
        self._name = name
        self._resource_group = resource_group
        self._location = location
        self._tags = tags or {}
        self._created_at = datetime.now()
        self._status = "Running"
        self._resource_id = f"/subscriptions/sub-{random.randint(1000,9999)}/resourceGroups/{resource_group}/providers/{self.__class__.__name__}/{name}"
        
        # Increment class variable
        AzureResource.total_resources += 1
    
    # Property decorators (getters) - Encapsulation
    @property
    def name(self):
        return self._name
    
    @property
    def status(self):
        return self._status
    
    @property
    def resource_id(self):
        return self._resource_id
    
    # Abstract method - must be implemented by subclasses
    @abstractmethod
    def calculate_cost(self):
        """Calculate monthly cost - each resource type implements differently"""
        pass
    
    # Concrete methods (shared by all resources)
    def start(self):
        """Start the resource"""
        if self._status == "Stopped":
            self._status = "Running"
            return f"✅ {self._name} started"
        return f"ℹ️  {self._name} is already running"
    
    def stop(self):
        """Stop the resource"""
        if self._status == "Running":
            self._status = "Stopped"
            return f"✅ {self._name} stopped"
        return f"ℹ️  {self._name} is already stopped"
    
    def add_tag(self, key, value):
        """Add a tag to the resource"""
        self._tags[key] = value
        return f"✅ Tag added: {key}={value}"
    
    def get_info(self):
        """Get resource information"""
        return {
            'name': self._name,
            'type': self.__class__.__name__,
            'resource_group': self._resource_group,
            'location': self._location,
            'status': self._status,
            'created': self._created_at.strftime('%Y-%m-%d'),
            'tags': self._tags
        }
    
    def __str__(self):
        """String representation"""
        return f"{self.__class__.__name__}(name='{self._name}', status='{self._status}')"
    
    def __repr__(self):
        """Developer representation"""
        return f"<{self.__class__.__name__} {self._name}>"

print("✅ Base class 'AzureResource' created")
print("   • Demonstrates: Abstract base class, encapsulation, properties")


# ============================================================================
# CELL 2: Concrete Resource Classes - Implementing Inheritance
# ============================================================================
print("\n" + "=" * 70)
print("🔨 CREATING CONCRETE RESOURCE CLASSES")
print("=" * 70)

class VirtualMachine(AzureResource):
    """
    Azure Virtual Machine
    Demonstrates: Inheritance, Method Overriding, Additional Properties
    """
    
    # Class variable for pricing
    VM_PRICING = {
        "Standard_B1s": 0.0104,
        "Standard_B2s": 0.0416,
        "Standard_D2s_v3": 0.096,
        "Standard_D4s_v3": 0.192,
        "Standard_E4s_v3": 0.252,
        "Standard_E8s_v3": 0.504
    }
    
    def __init__(self, name, resource_group, location, vm_size, os_type="Linux", tags=None):
        super().__init__(name, resource_group, location, tags)
        self._vm_size = vm_size
        self._os_type = os_type
        self._uptime_hours = 0
    
    @property
    def vm_size(self):
        return self._vm_size
    
    def calculate_cost(self, hours=730):  # 730 hours = 1 month
        """Calculate VM cost based on size and uptime"""
        if self._status == "Stopped":
            return 0  # Deallocated VMs don't incur compute costs
        
        hourly_rate = self.VM_PRICING.get(self._vm_size, 0.10)
        return hourly_rate * hours
    
    def resize(self, new_size):
        """Change VM size"""
        if new_size not in self.VM_PRICING:
            return f"❌ Invalid VM size: {new_size}"
        
        old_size = self._vm_size
        old_cost = self.calculate_cost()
        self._vm_size = new_size
        new_cost = self.calculate_cost()
        savings = old_cost - new_cost
        
        return f"✅ Resized from {old_size} to {new_size} (Monthly: ${old_cost:.2f} → ${new_cost:.2f}, Savings: ${savings:+.2f})"
    
    def restart(self):
        """Restart the VM"""
        self._status = "Restarting"
        self._status = "Running"
        return f"✅ {self._name} restarted"


class StorageAccount(AzureResource):
    """
    Azure Storage Account
    Demonstrates: Different implementation of abstract methods
    """
    
    TIER_PRICING = {
        "Hot": 0.0184,      # per GB/month
        "Cool": 0.01,       # per GB/month
        "Archive": 0.00099  # per GB/month
    }
    
    def __init__(self, name, resource_group, location, storage_gb=100, tier="Hot", tags=None):
        super().__init__(name, resource_group, location, tags)
        self._storage_gb = storage_gb
        self._tier = tier
    
    @property
    def tier(self):
        return self._tier
    
    @property
    def storage_gb(self):
        return self._storage_gb
    
    def calculate_cost(self, hours=730):
        """Calculate storage cost"""
        return self._storage_gb * self.TIER_PRICING[self._tier]
    
    def change_tier(self, new_tier):
        """Change access tier"""
        if new_tier not in self.TIER_PRICING:
            return f"❌ Invalid tier: {new_tier}"
        
        old_tier = self._tier
        old_cost = self.calculate_cost()
        self._tier = new_tier
        new_cost = self.calculate_cost()
        savings = old_cost - new_cost
        
        return f"✅ Tier changed from {old_tier} to {new_tier} (Monthly: ${old_cost:.2f} → ${new_cost:.2f}, Savings: ${savings:+.2f})"
    
    def add_storage(self, gb):
        """Increase storage capacity"""
        self._storage_gb += gb
        return f"✅ Added {gb}GB storage (Total: {self._storage_gb}GB)"


class SQLDatabase(AzureResource):
    """
    Azure SQL Database
    Demonstrates: More complex cost calculation
    """
    
    DTU_PRICING = {
        "Basic": 4.99,
        "S0": 15.00,
        "S1": 30.00,
        "S2": 75.00,
        "S3": 150.00,
        "P1": 465.00
    }
    
    def __init__(self, name, resource_group, location, tier="S0", storage_gb=250, tags=None):
        super().__init__(name, resource_group, location, tags)
        self._tier = tier
        self._storage_gb = storage_gb
        self._backup_enabled = True
    
    def calculate_cost(self, hours=730):
        """Calculate SQL DB cost (compute + storage)"""
        compute_cost = self.DTU_PRICING.get(self._tier, 30.00)
        storage_cost = self._storage_gb * 0.115  # $0.115 per GB/month
        backup_cost = 10 if self._backup_enabled else 0
        return compute_cost + storage_cost + backup_cost
    
    def scale_tier(self, new_tier):
        """Scale database tier"""
        if new_tier not in self.DTU_PRICING:
            return f"❌ Invalid tier: {new_tier}"
        
        old_tier = self._tier
        old_cost = self.calculate_cost()
        self._tier = new_tier
        new_cost = self.calculate_cost()
        
        return f"✅ Scaled from {old_tier} to {new_tier} (Monthly: ${old_cost:.2f} → ${new_cost:.2f})"


class AppService(AzureResource):
    """
    Azure App Service
    Demonstrates: Additional methods and state management
    """
    
    PLAN_PRICING = {
        "Free": 0,
        "Shared": 9.49,
        "Basic": 54.75,
        "Standard": 146.00,
        "Premium": 292.00
    }
    
    def __init__(self, name, resource_group, location, plan="Basic", instances=1, tags=None):
        super().__init__(name, resource_group, location, tags)
        self._plan = plan
        self._instances = instances
        self._auto_scale = False
    
    def calculate_cost(self, hours=730):
        """Calculate App Service cost"""
        return self.PLAN_PRICING[self._plan] * self._instances
    
    def scale_out(self, new_instance_count):
        """Scale out (add instances)"""
        if new_instance_count < 1 or new_instance_count > 10:
            return "❌ Instance count must be between 1 and 10"
        
        old_cost = self.calculate_cost()
        self._instances = new_instance_count
        new_cost = self.calculate_cost()
        
        return f"✅ Scaled to {new_instance_count} instances (Monthly: ${old_cost:.2f} → ${new_cost:.2f})"
    
    def enable_auto_scale(self, min_instances=1, max_instances=5):
        """Enable auto-scaling"""
        self._auto_scale = True
        self._min_instances = min_instances
        self._max_instances = max_instances
        return f"✅ Auto-scale enabled: {min_instances}-{max_instances} instances"


print("✅ Created 4 concrete resource classes:")
print("   • VirtualMachine - with resize() method")
print("   • StorageAccount - with change_tier() method")
print("   • SQLDatabase - with scale_tier() method")
print("   • AppService - with scale_out() and auto_scale methods")


# ============================================================================
# CELL 3: Resource Group Manager Class - Composition
# ============================================================================
print("\n" + "=" * 70)
print("📦 CREATING RESOURCE GROUP MANAGER")
print("=" * 70)

class ResourceGroup:
    """
    Azure Resource Group - manages multiple resources
    Demonstrates: Composition, Aggregation, Collection Management
    """
    
    def __init__(self, name, location):
        self._name = name
        self._location = location
        self._resources = []  # Composition - contains other objects
        self._created_at = datetime.now()
    
    @property
    def name(self):
        return self._name
    
    def add_resource(self, resource):
        """Add a resource to the group"""
        if not isinstance(resource, AzureResource):
            return "❌ Must be an AzureResource instance"
        
        self._resources.append(resource)
        return f"✅ Added {resource.name} to {self._name}"
    
    def remove_resource(self, resource_name):
        """Remove a resource by name"""
        self._resources = [r for r in self._resources if r.name != resource_name]
        return f"✅ Removed {resource_name} from {self._name}"
    
    def get_resource(self, name):
        """Find a resource by name"""
        for resource in self._resources:
            if resource.name == name:
                return resource
        return None
    
    def list_resources(self):
        """List all resources"""
        if not self._resources:
            return f"ℹ️  No resources in {self._name}"
        
        print(f"\n{'='*70}")
        print(f"📦 Resource Group: {self._name} ({self._location})")
        print(f"{'='*70}")
        print(f"{'Resource Name':<25} {'Type':<20} {'Status':<12} {'Monthly Cost':<15}")
        print(f"{'-'*70}")
        
        total_cost = 0
        for resource in self._resources:
            cost = resource.calculate_cost()
            total_cost += cost
            resource_type = resource.__class__.__name__
            print(f"{resource.name:<25} {resource_type:<20} {resource.status:<12} ${cost:>12.2f}")
        
        print(f"{'-'*70}")
        print(f"{'Total Resources: ' + str(len(self._resources)):<58} ${total_cost:>12.2f}")
        print(f"{'='*70}\n")
        
        return total_cost
    
    def total_cost(self):
        """Calculate total cost of all resources"""
        return sum(resource.calculate_cost() for resource in self._resources)
    
    def start_all(self):
        """Start all resources"""
        results = [resource.start() for resource in self._resources]
        return f"✅ Started all resources in {self._name}"
    
    def stop_all(self):
        """Stop all resources"""
        results = [resource.stop() for resource in self._resources]
        return f"✅ Stopped all resources in {self._name}"
    
    def get_resources_by_type(self, resource_type):
        """Filter resources by type"""
        return [r for r in self._resources if isinstance(r, resource_type)]
    
    def __len__(self):
        """Support len() function"""
        return len(self._resources)
    
    def __iter__(self):
        """Support iteration"""
        return iter(self._resources)
    
    def __str__(self):
        return f"ResourceGroup(name='{self._name}', resources={len(self._resources)})"


print("✅ ResourceGroup class created")
print("   • Demonstrates: Composition, collection management")
print("   • Supports: iteration, len(), resource filtering")


# ============================================================================
# CELL 4: Building a Complete Azure Environment
# ============================================================================
print("\n" + "=" * 70)
print("🏗️  BUILDING AZURE ENVIRONMENT")
print("=" * 70)

# Create resource groups
rg_production = ResourceGroup("rg-production", "East US")
rg_development = ResourceGroup("rg-development", "West US")

# Create Production resources
print("\n📦 Creating Production Resources...")

vm_web = VirtualMachine(
    "vm-web-prod-01",
    "rg-production",
    "East US",
    "Standard_D4s_v3",
    tags={"Environment": "Production", "Application": "Web"}
)

vm_db = VirtualMachine(
    "vm-db-prod-01",
    "rg-production",
    "East US",
    "Standard_E8s_v3",
    tags={"Environment": "Production", "Application": "Database"}
)

storage_data = StorageAccount(
    "stproddata001",
    "rg-production",
    "East US",
    storage_gb=1000,
    tier="Hot"
)

storage_backup = StorageAccount(
    "stprodbackup001",
    "rg-production",
    "East US",
    storage_gb=5000,
    tier="Cool"
)

sql_prod = SQLDatabase(
    "sqlprod001",
    "rg-production",
    "East US",
    tier="S3",
    storage_gb=500
)

app_prod = AppService(
    "app-prod-web",
    "rg-production",
    "East US",
    plan="Standard",
    instances=3
)

# Add to resource group
rg_production.add_resource(vm_web)
rg_production.add_resource(vm_db)
rg_production.add_resource(storage_data)
rg_production.add_resource(storage_backup)
rg_production.add_resource(sql_prod)
rg_production.add_resource(app_prod)

print(f"✅ Created {len(rg_production)} production resources")

# Create Development resources
print("\n📦 Creating Development Resources...")

vm_dev = VirtualMachine("vm-dev-01", "rg-development", "West US", "Standard_B2s")
storage_dev = StorageAccount("stdev001", "rg-development", "West US", 100, "Hot")
sql_dev = SQLDatabase("sqldev001", "rg-development", "West US", "Basic", 50)
app_dev = AppService("app-dev", "rg-development", "West US", "Basic", 1)

rg_development.add_resource(vm_dev)
rg_development.add_resource(storage_dev)
rg_development.add_resource(sql_dev)
rg_development.add_resource(app_dev)

print(f"✅ Created {len(rg_development)} development resources")

print(f"\n📊 Total Azure Resources: {AzureResource.total_resources}")


# ============================================================================
# CELL 5: Resource Operations - Polymorphism in Action
# ============================================================================
print("\n" + "=" * 70)
print("⚙️  PERFORMING RESOURCE OPERATIONS")
print("=" * 70)

# Display current state
print("\n📋 CURRENT ENVIRONMENT STATE:")
print("\nProduction:")
prod_cost = rg_production.list_resources()

print("Development:")
dev_cost = rg_development.list_resources()

print(f"💰 Total Monthly Cost: ${prod_cost + dev_cost:.2f}")

# Perform optimization operations
print("\n" + "=" * 70)
print("🔧 OPTIMIZATION OPERATIONS")
print("=" * 70)

print("\n1️⃣ Resizing oversized VMs...")
print(vm_web.resize("Standard_D2s_v3"))  # Downsize web server

print("\n2️⃣ Optimizing storage tiers...")
print(storage_backup.change_tier("Archive"))  # Move backups to cheapest tier

print("\n3️⃣ Scaling down development environment...")
print(app_dev.scale_out(1))  # Ensure dev uses only 1 instance
print(sql_dev.scale_tier("Basic"))  # Use smallest SQL tier

print("\n4️⃣ Stopping non-critical resources...")
print(vm_dev.stop())  # Stop dev VM when not in use

print("\n5️⃣ Enabling auto-scale for production app...")
print(app_prod.enable_auto_scale(min_instances=2, max_instances=5))


# ============================================================================
# CELL 6: Cost Analysis After Optimization
# ============================================================================
print("\n" + "=" * 70)
print("📊 COST ANALYSIS AFTER OPTIMIZATION")
print("=" * 70)

print("\n📋 OPTIMIZED ENVIRONMENT STATE:")
print("\nProduction:")
new_prod_cost = rg_production.list_resources()

print("Development:")
new_dev_cost = rg_development.list_resources()

new_total_cost = new_prod_cost + new_dev_cost
old_total_cost = prod_cost + dev_cost

savings = old_total_cost - new_total_cost
savings_pct = (savings / old_total_cost) * 100

print(f"\n{'='*70}")
print("💰 COST COMPARISON")
print(f"{'='*70}")
print(f"Before Optimization: ${old_total_cost:>10.2f}/month")
print(f"After Optimization:  ${new_total_cost:>10.2f}/month")
print(f"{'-'*70}")
print(f"Monthly Savings:     ${savings:>10.2f} ({savings_pct:.1f}%)")
print(f"Annual Savings:      ${savings * 12:>10.2f}")
print(f"{'='*70}")


# ============================================================================
# CELL 7: Advanced OOP Features - Special Methods
# ============================================================================
print("\n" + "=" * 70)
print("🎓 DEMONSTRATING ADVANCED OOP FEATURES")
print("=" * 70)

print("\n1️⃣ Using __str__ and __repr__:")
print(f"String representation: {vm_web}")
print(f"Developer representation: {repr(vm_web)}")

print("\n2️⃣ Iteration over resource group:")
print("Iterating through production resources:")
for resource in rg_production:
    print(f"  • {resource.name} ({resource.__class__.__name__})")

print("\n3️⃣ Using len() on resource group:")
print(f"Production has {len(rg_production)} resources")
print(f"Development has {len(rg_development)} resources")

print("\n4️⃣ Property access (encapsulation):")
print(f"VM Name (via property): {vm_web.name}")
print(f"VM Status (via property): {vm_web.status}")
print(f"VM Size (via property): {vm_web.vm_size}")

print("\n5️⃣ Type checking and filtering:")
all_vms = rg_production.get_resources_by_type(VirtualMachine)
all_storage = rg_production.get_resources_by_type(StorageAccount)
print(f"Production VMs: {len(all_vms)}")
print(f"Production Storage Accounts: {len(all_storage)}")

print("\n6️⃣ Polymorphism - calculate_cost() works for all resource types:")
for resource in rg_production:
    cost = resource.calculate_cost()  # Same method, different implementations
    print(f"  {resource.name}: ${cost:.2f}/month")


# ============================================================================
# CELL 8: Create Comprehensive Report
# ============================================================================
print("\n" + "=" * 70)
print("📋 GENERATING COMPREHENSIVE REPORT")
print("=" * 70)

# Collect all resources
all_resources = []
for rg in [rg_production, rg_development]:
    for resource in rg:
        info = resource.get_info()
        info['resource_group'] = rg.name
        info['monthly_cost'] = resource.calculate_cost()
        all_resources.append(info)

# Create DataFrame for analysis
import pandas as pd
df_resources = pd.DataFrame(all_resources)

print("\n📊 RESOURCE INVENTORY:")
print(df_resources.to_string(index=False))

# Summary by type
print("\n📈 SUMMARY BY RESOURCE TYPE:")
summary_by_type = df_resources.groupby('type').agg({
    'name': 'count',
    'monthly_cost': 'sum'
}).round(2)
summary_by_type.columns = ['Count', 'Total_Monthly_Cost']
print(summary_by_type)

# Summary by resource group
print("\n📈 SUMMARY BY RESOURCE GROUP:")
summary_by_rg = df_resources.groupby('resource_group').agg({
    'name': 'count',
    'monthly_cost': 'sum'
}).round(2)
summary_by_rg.columns = ['Resource_Count', 'Total_Monthly_Cost']
print(summary_by_rg)

# Export to CSV
df_resources.to_csv('azure_resource_inventory.csv', index=False)
print("\n✅ Resource inventory exported to 'azure_resource_inventory.csv'")

# Create visualization
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Cost by Resource Type
summary_by_type.plot(kind='bar', y='Total_Monthly_Cost', ax=axes[0], 
                     color='#0078D4', legend=False, edgecolor='black')
axes[0].set_title('Monthly Cost by Resource Type', fontweight='bold', fontsize=12)
axes[0].set_xlabel('Resource Type', fontsize=10)
axes[0].set_ylabel('Monthly Cost ($)', fontsize=10)
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(axis='y', alpha=0.3)

# Plot 2: Resource Distribution
type_counts = df_resources['type'].value_counts()
axes[1].pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%',
           startangle=90, colors=plt.cm.Set3.colors)
axes[1].set_title('Resource Distribution by Type', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('azure_oop_resource_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Visualization saved as 'azure_oop_resource_analysis.png'")

print("\n" + "=" * 70)
print("🎓 LAB 5 COMPLETE!")
print("=" * 70)
print("\nOOP Concepts Demonstrated:")
print("  ✅ Classes and Objects")
print("  ✅ Inheritance (Abstract base class → Concrete classes)")
print("  ✅ Encapsulation (Private variables, properties)")
print("  ✅ Polymorphism (calculate_cost() for different resource types)")
print("  ✅ Composition (ResourceGroup contains Resources)")
print("  ✅ Abstract methods (@abstractmethod)")
print("  ✅ Special methods (__str__, __repr__, __len__, __iter__)")
print("  ✅ Class vs Instance variables")
print("  ✅ Method overriding")
print("  ✅ Property decorators (@property)")
print("\nReal-World Skills:")
print("  ✅ Modular, reusable code design")
print("  ✅ Clean code architecture")
print("  ✅ Type hierarchies")
print("  ✅ Resource management patterns")
print("=" * 70)